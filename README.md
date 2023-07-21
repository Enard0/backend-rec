## Installation
Install docker-compose and run app with
```bash
sudo docker-compose up -d --build
```
## Models
### Task
| Field | Type | Description|
|--|--|--|
| `title` | text | Title of task, can't be empty |
| `description` | text | Description of task, can be empty |
| `status` | int | Status of task <br>`0 New`<br>`1 in progress`<br>`2 Completed` |
| `users` | [User] | Array of Users to add to task |

### History
| Field | Type | Description|
|--|--|--|
| `date` | ISO format | Time of action |
| `task_id` | int | id of task |
| `action` | int | Action taken upon <br>`0 Created`<br>`1 Modify`<br>`2 Removal` |
| `title` | text | Title of task, can't be empty |
| `description` | text | Description of task, can be empty |
| `status` | int | Status of task <br>`0 New`<br>`1 in progress`<br>`2 Completed` |
| `users` | [User] | Array of Users to add to task |
## Usage
### Create superuser
Run in bash
```bash
sudo docker-compose exec web python3 manage.py createsuperuser
```

## Task api

### Get all tasks
**GET /tasks**<br>
Returns json with all task models

### Filter tasks
**GET /tasks?key=value**<br>
Returns json with filtered values.
Possible keys:
| Key | Type | Description |
|--|--|--|
| title | text | Exact title of task |
| description | text | Text that has to be in description |
| status | int | `0 New`<br>`1 in progress`<br>`2 Completed`  |
| users | User | Array of User objects |

### Add task
**POST /tasks**<br>
Returns json with object on succes
Takes data in json
Example data:
```json
{
    "title": "Task",
    "description": "Example Task",
    "status": 0,
    "users": []
}
```

### Modify task
**PUT /tasks/<id>**<br>
Returns json with object on succes
Takes the same data as Post method

### Remove task
**DELETE /task/<id>**<br>
Returns 204 response on success


## History api

### Get all history entry
**GET /history**<br>
Returns json with all task models

### Filter history entry
**GET /tasks?key=value**<br>
Returns json with filtered values.
Possible keys:
| Key | Type | Description|
|--|--|--|
| id | int | Id of Task object |
| action | int | Action taken upon Task object<br>`0 Created`<br>`1 Modify`<br>`2 Removal` |
| when | UNIX timestamp or ISO format | Show state of Task at given time  |