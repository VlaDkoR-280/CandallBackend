from src.db_handler.database import get_groups
import asyncio
if __name__ == '__main__':
    
    groups_id = asyncio.run(get_groups())
    
    for i, id in enumerate(groups_id):
        print(f"{i}. {id}")