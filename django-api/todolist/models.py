from django.db import models

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'task'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status
        }

