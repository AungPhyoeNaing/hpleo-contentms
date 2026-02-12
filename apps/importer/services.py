import httpx
import logging
from django.utils import timezone
from django.utils.html import strip_tags
from apps.videos.models import Video, Category, Episode
from apps.importer.models import ImportLog

logger = logging.getLogger(__name__)

class CaobizyImporter:
    def __init__(self, api_url="https://www.caobizy.com/api.php/provide/vod/"):
        self.api_url = api_url

    async def fetch_videos(self, page=1):
        params = {
            "ac": "videolist",
            "pg": page,
            "t": "",
            "h": "",
            "ids": "",
            "wd": "",
        }
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(self.api_url, params=params, timeout=15.0)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Failed to fetch videos from {self.api_url}: {e}")
                return None

    async def run_import(self, pages=1):
        log = await ImportLog.objects.acreate(status='running')
        success_count = 0
        fail_count = 0
        
        try:
            # First fetch to get total pages if needed, but we just loop pages for now
            for page in range(1, pages + 1):
                data = await self.fetch_videos(page)
                if not data or 'list' not in data:
                    logger.warning(f"No data found for page {page}")
                    break
                
                video_list = data.get('list', [])
                if not video_list:
                    break

                for item in video_list:
                    try:
                        await self.process_item(item)
                        success_count += 1
                    except Exception as e:
                        fail_count += 1
                        logger.error(f"Error processing item {item.get('vod_id')}: {e}")
            
            log.status = 'completed'
        except Exception as e:
            log.status = 'failed'
            log.details = str(e)
            logger.error(f"Import failed: {e}")
        finally:
            log.finished_at = timezone.now()
            log.success_count = success_count
            log.fail_count = fail_count
            await log.asave()
        
        return log

    async def process_item(self, item):
        # 1. Category
        category_name = item.get('type_name')
        category_id = item.get('type_id')
        
        if category_name:
            category, _ = await Category.objects.aget_or_create(
                name=category_name,
                defaults={'external_id': category_id}
            )
        else:
            category = None

        # 2. Video
        vod_id = item.get('vod_id')
        if not vod_id:
            raise ValueError("Missing vod_id")

        defaults = {
            'title': item.get('vod_name'),
            'thumbnail_url': item.get('vod_pic'),
            'description': strip_tags(item.get('vod_content', '')),
            'category': category,
        }
        
        video, created = await Video.objects.aupdate_or_create(
            external_id=vod_id,
            defaults=defaults
        )

        # 3. Parse Episodes
        vod_play_url = item.get('vod_play_url', '')
        await self.process_episodes(video, vod_play_url)

    async def process_episodes(self, video, vod_play_url):
        # Remove existing episodes to ensure sync
        await Episode.objects.filter(video=video).adelete()
        
        if not vod_play_url:
            return

        # Parsing Logic: Split by '#' then '$'
        # Example: Ep1$https://link.m3u8#Ep2$https://link.m3u8
        episode_strings = vod_play_url.split('#')
        episodes_to_create = []
        
        for index, ep_str in enumerate(episode_strings):
            if not ep_str.strip():
                continue
                
            parts = ep_str.split('$')
            if len(parts) >= 2:
                label = parts[0]
                url = parts[1]
            else:
                label = f"Episode {index+1}"
                url = parts[0] # Fallback if no label
            
            # Basic validation
            if not url.startswith('http'):
                # Handle cases where url might not be valid or is just a label
                continue

            episodes_to_create.append(Episode(
                video=video,
                label=label,
                url=url,
                index=index
            ))
        
        if episodes_to_create:
            await Episode.objects.abulk_create(episodes_to_create)
