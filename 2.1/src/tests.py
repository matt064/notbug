import unittest
import json

from db import db
from app import app
from models import Task

class TaskListTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context() 
        self.app_context.push()

        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_get_tasks(self):
        "test pobierania listy zadań"

        self.app.post('/', 
                    data=json.dumps({'title': 'Zadanie 1', 'content': 'Opis zadania 1', 'done': True}),
                    content_type='application/json')
        self.app.post('/', 
                    data=json.dumps({'title': 'Zadanie 2', 'content': 'Opis zadania 2'}),
                    content_type='application/json')
        self.app.post('/', 
                    data=json.dumps({'title': 'Zadanie 3', 'content': 'Opis zadania 3'}),
                    content_type='application/json')


        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)  
        self.assertEqual(data[0]['title'], 'Zadanie 1')
        self.assertEqual(data[1]['title'], 'Zadanie 2')
        self.assertEqual(data[2]['title'], 'Zadanie 3')

    def test_get_single_task(self):
        "test pobierania pojedynczego zadania"
        response = self.app.post('/', data=json.dumps({'title': 'Test Task', 'content': 'opis opis'}), content_type='application/json')
        task_id = json.loads(response.data)['id']

        # Pobieramy utworzone zadanieas
        response = self.app.get(f'/{task_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], task_id)
        self.assertEqual(data['title'], 'Test Task')
    

    def test_create_task(self):
        "test dodawania nowego zadania"
        response = self.app.post('/', 
                                 data=json.dumps({'title': 'Zadanie 1', 'content': 'Opis'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Zadanie 1')
        self.assertEqual(data['content'], 'Opis')
        self.assertFalse(data['done'])


    def test_update_task(self):
        "test aktualizacji zadania"
        # dodanie zadania
        response = self.app.post('/', 
                                 data=json.dumps({'title': 'Zadanie 1', 'content': 'Opis zadania 1'}),
                                 content_type='application/json')
        task_id = json.loads(response.data)['id']
        
        # aktualizacja zadania
        response = self.app.put(f'/{task_id}', 
                                data=json.dumps({'title': 'Zadanie 1aaaa', 'content': 'Nowy opis'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Zadanie 1aaaa')

    
    def test_delete_task(self):
        "test usuwania zadania"
        response = self.app.post('/', 
                                 data=json.dumps({'title': 'Zadanie 1', 'content': 'Opis'}),
                                 content_type='application/json')
        task_id = json.loads(response.data)['id']
        
        # Usuwamy zadanie
        response = self.app.delete(f'/{task_id}')
        self.assertEqual(response.status_code, 204)

        # Sprawdzamy, czy zadanie zostało usunięte
        response = self.app.get(f'/{task_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()