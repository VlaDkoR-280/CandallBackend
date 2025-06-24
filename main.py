from src.db_handler.database import get_groups
import asyncio
if __name__ == '__main__':
    
    groups_id = asyncio.run(get_groups())
    
    print(groups_id)