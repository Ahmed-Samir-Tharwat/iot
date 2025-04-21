import asyncio
from prisma import Prisma
from datetime import datetime

async def main() -> None:
    prisma = Prisma()
    await prisma.connect()
    
#     model User {
#   id       String @id @default(uuid())
#   name     String
#   username String @unique
#   password String

#   img      String   @default("https://cdn.landesa.org/wp-content/uploads/default-user-image.png")
#   prevImgs String[]

#   role UserRole @default(student)

#   licensePlate String?

#   student    Student?
#   teacher    Teacher?
#   controller Controller?
#   security   Security?
#   admin      Admin?

#   sessions Session[]

#   encodedImageData String?
# }

    # write your queries here
    user = await prisma.user.create(
        data={
            'img':'./uploads/messi.jpg'
        },
    )
    # user = await prisma.user.create(
    #     data={
    #         'name': 'Robert',
    #         'username': 'Robert12',
    #         'password': 'robert@craigie.dev'
    #     },
    # )
#     model Lecture {
#   id       String    @id @default(uuid())
#   courseId String
#   time     DateTime
#   duration Int
#   ended    DateTime?
#   location String

#   attendees LectureAttendees[]
#   imgs      LectureImage[]

#   course Course @relation(fields: [courseId], references: [id], onDelete: Cascade)
# }

# model Course {
#   id          String  @id @default(uuid())
#   name        String
#   code        String  @unique
#   creditHours Int
#   content     String?

#   students CourseProfile[]

#   teachers Teacher[]
#   lectures Lecture[]
# }

    # Course = await prisma.course.create(
    #     data={
    #         'id':'1',
    #         'name': 'math',
    #         'code': '12345',
    #         'creditHours': 3
    #     },
    # )


    
    # Lecture = await prisma.lecture.create(
    #     data={
    #         'id':'1',
    #         'courseId': '1',
    #         'time': datetime.fromisoformat('2024-12-01T15:30:00'),
    #         'duration': 2,
    #         'location': 'HALL A',
    #     }, # type: ignore
    # )
    


    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())