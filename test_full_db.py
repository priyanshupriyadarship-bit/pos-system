from backend.models.database import SessionLocal
from backend.models.user_model import User
from backend.models.task_model import Task, TaskPriority, TaskStatus
import uuid

db = SessionLocal()

# Create user
user = User(
    id=str(uuid.uuid4()),
    email='priyanshu@aiml.com',
    username='priyanshu',
    full_name='Priyanshu Priyadarshi',
    timezone='Asia/Kolkata'
)
db.add(user)
db.commit()
print(f'✅ User created: {user.email}')

# Create task
task = Task(
    id=str(uuid.uuid4()),
    user_id=user.id,
    title='Complete deepfake detection project',
    description='Train VideoMAE model',
    priority=TaskPriority.HIGH,
    status=TaskStatus.IN_PROGRESS,
    avatar_name='Businessman',
    xp_reward=50
)
db.add(task)
db.commit()
print(f'✅ Task created: {task.title}')

# Update avatar stats
user.update_avatar_stats('Businessman', 50)
db.commit()
print(f'✅ Avatar stats: {user.avatar_stats}')

# Query counts
print(f'✅ Total users: {db.query(User).count()}')
print(f'✅ Total tasks: {db.query(Task).count()}')

db.close()
print('🎉 Full database test PASSED!')
