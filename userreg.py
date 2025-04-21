import asyncio
from prisma import Prisma
from prisma.models import User
from datetime import datetime

prisma = Prisma()

async def register_user(name: str, username: str, password: str) -> User:
    # Check if the username is already taken
    existing_user = await prisma.user.find_first(where={"username": username})
    if existing_user:
        raise ValueError("Username is already taken.")
    
    # Create a new user
    user = await prisma.user.create(
        data={
            "name": name,
            "username": username,
            "password": password,
        },
    )
    return user

async def login_user(username: str, password: str) -> User:
    # Check if the user exists and the password matches
    user = await prisma.user.find_first(where={"username": username})
    if not user or user.password != password:
        raise ValueError("Invalid username or password.")
    return user

async def main():
    await prisma.connect()
    
    # Example: Register a new user
    try:
        user = await register_user("John Doe", "johndoe", "password123")
        print(f"User registered: {user.name}")
    except ValueError as e:
        print(e)

    # Example: Login a user
    try:
        user = await login_user("johndoe", "password123")
        print(f"User logged in: {user.name}")
    except ValueError as e:
        print(e)

    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
