# Created by: Izram Khan
# Date completed: 14-Dec-2024
# License: Feel free to use it's all yours
# ____________________________________________________________________________________________________
import random
import json
from datetime import datetime, timedelta
from collections import Counter
import csv
import os
import time

def load_task():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_task(tasks):
    with open('tasks.json','w') as f:
        json.dump(tasks, f, indent=3)

# Helper funcs for add_task() and update_task(): 1 - get_valid_date 2 - get-valid_priority 3 - get_input 4 - get_tag
def get_valid_date(prompt):
    while True:
        date = input(prompt).strip()
        try:
            datetime.strptime(date,'%Y/%m/%d')
            return date
        except ValueError:
            print('\n❌ Error: Invalid date! User fromat YYYY/MM/DD. Example: 2008/08/13.')

def get_valid_priority(prompt):
    valid_priorities = ['high','medium','low']
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_priorities:
            return user_input
        print('\n❌ Error: Invalid priority! Choose high/medium/low.')

def get_input(prompt, error_msg):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print(error_msg)

def add_task():
    tasks = load_task()
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|          NEW TASK           |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
     
    title = get_input("\nEnter the task title: ", "\n❌ Title cannot be empty!")
    description = get_input("\nEnter description: ", "\n❌ Description cannot be empty!")
    priority = get_valid_priority("\nEnter priority (low/medium/high): ")
    due_date = get_valid_date("\nEnter due date (YYYY/MM/DD): ")
    tag = get_input('\nEnter tags i.e, gaming, study, sports: ','\n❌ Tags cannot be empty!')
    task_id = str(random.randint(10000000, 999999999))

    task = {
        'id': task_id,
        'title': title.title(),
        'priority': priority,
        'due date': due_date,
        'done': False,
        'description': description,
        'tag': tag
            }
    
    tasks.append(task)
    save_task(tasks)
    print(f'\n✅ - Task :[{title.title()}] saved with ID: {task_id}')
    time.sleep(1)

def delete_task():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|         DELETE TASK         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')

    tasks= load_task()
    while True:
        id_check = input('\nEnter ID to delete task: ')
        if id_check == '0':
            print('\n🛑 - Stopped deleting!')
            break
        for dict in tasks:
            if dict['id'] == id_check:
                confirm = input('\nAre you sure (y/n): ').strip().lower()
                if confirm == 'y':
                    tasks.remove(dict)
                    save_task(tasks)
                    print(f'\n✅ Task: [{dict['title'].title()}] was removed!')
                    return
                elif confirm == 'n':
                    print('\n🛑 - Stopped deleting!!')
                    return
                else:
                    print('\n❌ - Error: Enter (y / n)!')
        print('\n❌ - Error: Id does not match!')
    time.sleep(1)

def mark_task():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|          MARK TASK          |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')

    tasks= load_task()
    while True:
        id_check = input('\nEnter ID to mark done: ')
        if id_check == '0':
            print('\n🛑 - Stopped marking down!')
            break
        for dict in tasks:
            if dict['id'] == id_check:
                if dict['done'] == True:
                    print(f'\n🛑 - Task: [{dict['title'].title()}] is already marked as done!')
                    return
                dict['done'] = True
                save_task(tasks)
                print(f'\n✅ Task: [{dict['title'].title()}] marked done!')
                return
        print('\n❌ Error: Id does not match!')
    time.sleep(1)

def view_all_tasks():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|       VIEW ALL TASK         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')

    tasks = load_task()
    all_tasks = [t for t in tasks]
  
    headers = f'{'ID':<10} {'Title':<15} {'Priority':<10} {'Due Date':<15} {'Done':<5} {'Tags':<15} {'Description'}'

    print(headers)
    print('-'*95)  
    
    if all_tasks:
        for t in all_tasks:
            done = '✅' if t['done'] else '❌'
            priority = '🔴' if t['priority'] == 'high' else '🟡' if t['priority'] == 'medium' else '🟢'
            print(f"{t['id']:<10} {t['title']:<15} {priority:<10} {t['due date']:<15} {done:<5} {t['tag']:<15} {t['description']}")
    else:
        print("🛑 - No task created yet!")
    time.sleep(1)

def update_task():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|         UPDATE TASK         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')

    tasks = load_task()
    while True:
        id_check = input('\nEnter ID to update: ')
        if id_check == '0':
            print('\n🛑 - Updating was stopped!')
            break

        task_to_update = None
        for t in tasks:
            if t['id'] == id_check:
                task_to_update = t
                break
        
        if not task_to_update:
            print('\n❌ - Error: ID does not exist!')
            continue

        print('\n1. Update title')
        print('2. Update description')
        print('3. Update priority')
        print('4. Update due date')
        print('5. Update tag')

        user_input = input('\nEnter (1 - 4): ')

        if user_input == '1':
            new_title = get_input("\nEnter the new task title: ", "\n❌ Title cannot be empty!")
            task_to_update['title'] = new_title
            print(f'\n✅ - New title: [{new_title.title()}] updated!')
            
        elif user_input == '2':
            new_description = get_input("\nEnter description: ", "\n❌ Description cannot be empty!")
            task_to_update['description'] = new_description
            print(f'\n✅ - New description: [{new_description}] updated!')
        
        elif user_input == '3':
            new_priority = get_valid_priority("\nEnter priority (low/medium/high): ")
            task_to_update['priority'] = new_priority
            print(f'\n✅ New priority: [{new_priority}] updated!')

        elif user_input == '4':
            new_due_date = get_valid_date("\nEnter due date (YYYY/MM/DD): ")
            task_to_update['due date'] = new_due_date
            print(f'\n✅ New due date: [{new_due_date}] updated!')
            
        elif user_input == '5':
            new_tag = get_input('\nEnter new tag: ', '\n❌ Tag cannot be empty!')
            task_to_update['tag'] = new_tag
            print(f'\n✅ New tag: [{new_tag}] updated')
            
        else:
            print('\n❌ - Error: Enter (1 - 4) or 0 to stop!')

        save_task(tasks)
        break
    time.sleep(1)

def filter_by_priority():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|      FILTER BY PRIORITY      |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    
    tasks = load_task()

    headers = f'{'ID':<10} {'Title':<15} {'Priority':<10} {'Due Date':<15} {'Done':<5} {'Tags':<15} {'Description'}'

    while True: 
        priority = input('\nEnter (high / medium / low): ').lower()

        if priority == '0':
            print('\n🛑 - Filtering Stopped!')
            break

        pri_tasks = [t for t in tasks if t['priority'] == priority]

        if priority in ['high', 'medium', 'low']:
            print(headers)
            print("-" * 95)
            if pri_tasks:
                for t in pri_tasks:
                    done = '✅' if t['done'] else '❌'
                    priority = '🔴' if t['priority'] == 'high' else '🟡' if t['priority'] == 'medium' else '🟢'
                    print(f"{t['id']:<10} {t['title']:<15} {priority:<10} {t['due date']:<15} {done:<5} {t['tag']:<15} {t['description']}")
            else:
                print(f"🛑 - No task is prioritized as {priority.lower()} yet!")
            break
        else:
            print('\n❌ - Error: Enter (high / medium / low)!')
    time.sleep(1)

def filter_by_tag():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|        FILTER BY TAG         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    
    tasks = load_task()

    headers = f'{'ID':<10} {'Title':<15} {'Priority':<10} {'Due Date':<15} {'Done':<5} {'Tags':<15} {'Description'}'

    while True:
        tag = input('\nEnter the tag: ').lower()

        if tag == '0':
            print('\n🛑 - Filtering stopped!')
            break

        tasks_tag = [t for t in tasks if tag in t['tag']]

        print(headers)
        print('-' * 95)
        if tasks_tag:
            for t in tasks_tag:
                done = '✅' if t['done'] else '❌'
                priority = '🔴' if t['priority'] == 'high' else '🟡' if t['priority'] == 'medium' else '🟢'
                print(f"{t['id']:<10} {t['title']:<15} {priority:<10} {t['due date']:<15} {done:<5} {t['tag']:<15} {t['description']}")
            break
        else:
            print(f'\n❌ - Error: No such tag as [{tag.lower()}]')
    time.sleep(1)

def filter_by_done():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|       FILtER BY STATUS       |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    
    tasks = load_task()

    headers = f'{'ID':<10} {'Title':<15} {'Priority':<10} {'Due Date':<15} {'Done':<5} {'Tags':<15} {'Description'}'

    while True:
        status = input('\nEnter status (true / false): ').lower()

        if status == '0':
            print('🛑 - Filtering stopped!')
            break

        elif status == 'true':
            status = True
        elif status == 'false':
            status = False
        else:
            print('\n❌ - Error: Enter (true / false)!')
            continue

        task_status = [t for t in tasks if t['done'] == status]

        print(headers)
        print('-' * 95)
        if task_status:
            for t in task_status:
                done = '✅' if t['done'] else '❌'
                priority = '🔴' if t['priority'] == 'high' else '🟡' if t['priority'] == 'medium' else '🟢'
                print(f"{t['id']:<10} {t['title']:<15} {priority:<10} {t['due date']:<15} {done:<5} {t['tag']:<15} {t['description']}")
            break
        else:
            print(f'\n❌ - Error: No task avaliable!')
            break
    time.sleep(1)

def search_task():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|         SEARCH TASK         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    
    tasks = load_task()
    
    while True:
        search = input('\nEnter some words from title or description: ')
        all_matchings = [t for t in tasks if search in t['title'] or search in t['description']]

        headers = f'{'ID':<10} {'Title':<15} {'Priority':<12} {'Due Date':<15} {'Description'}'
        print('\n')
        print(headers)
        print('-'*95)
        if all_matchings:
            for t in all_matchings:
                print(f'{t['id']:<10} {t['title']:<15} {t['priority']:<12} {t['due date']:<15} {t['description']}')
            return
        print('\n🛑 - Error: No result found!')    
        break
    time.sleep(1)
            
# Helpers for sort_tasks()
def sort_by_title(tasks, reverse=False):
    tasks.sort(key=lambda t: t['title'].lower(), reverse=reverse)

def sort_by_priority(tasks, reverse=False):
    priority_order = {'high': 1, 'medium': 2, 'low': 3}
    tasks.sort(key=lambda t: priority_order[t['priority']], reverse=reverse)

def sort_by_due_date(tasks, reverse=False):
    tasks.sort(key=lambda t: t['due date'], reverse=reverse)

def sort_by_done(tasks, reverse=False):
    tasks.sort(key=lambda t: t['done'], reverse=reverse)            

def get_order(prompt='Enter (1 = Ascending / 2 = Descending): '):
    while True:
        order = input(prompt)
        if order in ['1', '2']:
            return order == '2'  # True if descending
        print('\n❌ - Enter (1 / 2)!')

def sort_tasks():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|          SORT TASKS         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    
    tasks = load_task()
    print('\n1. A - Z')
    print('2. Z - A')
    print('3. By priority')
    print('4. By due date')
    print('5. Completed first or pending first')

    while True:
        sort_by = input('\nEnter (1 - 5): ')
        if sort_by == '1':
            sort_by_title(tasks)
            print('\n✅ - Tasks sorted (A - Z)!')

        elif sort_by == '2':
            sort_by_title(tasks, reverse=True)
            print('\n✅ - Tasks sorted (Z - A)!')
        
        elif sort_by == '3': 
            reverse = get_order('\nHigh -> Low (1). Low -> High (2): ')
            sort_by_priority(tasks, reverse=reverse)
            print('\n✅ - Tasks sorted by priority!')               

        elif sort_by == '4':
            sort_by_due_date(tasks)
            print('\n✅ - Tasks sorted by due date!')

        elif sort_by == '5':  
            reverse = get_order('\nPending first -> 1. Completed first -> 2: ')
            sort_by_done(tasks, reverse=reverse)
            print('\n✅ Tasks sorted by completion status!')

        else:
            print('\n❌ Error: Please enter (1 - 5)!')

        save_task(tasks)
        break
    time.sleep(1)

# Helper funcs for statistics_screen(): 1 - get_task_dues 2 - count_tags
def get_task_dues():
    tasks = load_task()

    today = datetime.today().date()
    week_later = today + timedelta(days=7)
    month_later = today + timedelta(days=30)

    tasks_due_today = []
    tasks_due_this_week = []
    tasks_due_this_month = []
    tasks_overdue = []

    for t in tasks:
        # Convert string to datetime object (real-time)
        due_date = datetime.strptime(t['due date'], "%Y/%m/%d").date()
        
        if due_date == today:
            tasks_due_today.append(t)
        elif today < due_date <= week_later:
            tasks_due_this_week.append(t)
        elif today < due_date <= month_later:
            tasks_due_this_month.append(t)
        elif due_date < today:
            tasks_overdue.append(t)

    print(f'Due Today:      {len(tasks_due_today)}')
    print(f'Due This Week:  {len(tasks_due_this_week)}')
    print(f'Due This Month: {len(tasks_due_this_month)}')
    print(f'OverDue:        {len(tasks_overdue)}')

def count_tags():
    tasks = load_task()
    tags = []

    for t in tasks:
        if 'tag' in t and t['tag']:
            tags.append(t['tag'])

    counts = Counter(tags)

    for key, value in counts.items():
        print(f'{value} - {key}')

def statistics_screen():
    tasks = load_task()

    total_tasks = [t for t in tasks]
    completed_tasks = [t for t in tasks if t['done']]
    pending_tasks = [t for t in tasks if not t['done']]

    completion_rate = (len(pending_tasks) * 100) / len(total_tasks)
    remaining_rate = (100 - completion_rate)

    high_pri_tasks = [t for t in tasks if t['priority'] == 'high']
    med_pri_tasks = [t for t in tasks if t['priority'] == 'medium']
    low_pri_tasks = [t for t in tasks if t['priority'] == 'low']
    
    high_pri_rate = (len(high_pri_tasks) * 100) / len(total_tasks)
    med_pri_rate = (len(med_pri_tasks) * 100) / len(total_tasks)
    low_pri_rate = (len(low_pri_tasks) * 100) / len(total_tasks)

    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|         STATISTICS          |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    print(f'Total Tasks:       {len(total_tasks)}')
    print(f'Task Completed:    {len(completed_tasks)}')
    print(f'Task Pending:      {len(pending_tasks)}')
    print(f'\nCompletion Rate:   {completion_rate:.2f}%')
    print(f'Remaining Rate:    {remaining_rate:.2f}%')

    print('\n||━━━━━ PRIORITY_WISE ━━━━━||\n')
    print(f'High Priority:   {len(high_pri_tasks)} | {high_pri_rate:.2f}%')
    print(f'Medium Priority: {len(med_pri_tasks)} | {med_pri_rate:.2f}%')
    print(f'Low Priority:    {len(low_pri_tasks)} | {low_pri_rate:.2f}%')

    print('\n||━━━━━ TASKS_DUES ━━━━━||\n')
    get_task_dues()

    print('\n||━━━━━ TASKS_BY_TAGS ━━━━━||\n')
    count_tags()
    time.sleep(1)

def export_tasks():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|        EXPORT TASKS         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    tasks = load_task()
    print('\nYou can import you date as following:')
    print('1. .txt file')
    print('2. .csv file')
    path = os.getcwd()
    while True:
        format = input('\nEnter (1 / 2): ')

        if format == '1':
            headers = f'{'ID':<10} {'Title':<15} {'Priority':<10} {'Due Date':<15} {'Done':<5} {'Tags':<15} {'Description'}'
            with open('tasks.txt', 'w', encoding='utf-8') as f:
                f.write(headers + '\n')
                f.write('-'*95 + '\n')
                for t in tasks:
                    done = '✅' if t['done'] else '❌'
                    priority = '🔴' if t['priority'] == 'high' else '🟡' if t['priority'] == 'medium' else '🟢'
                    f.write(f"{t['id']:<10} {t['title']:<15} {priority:<10} {t['due date']:<15} {done:<5} {t['tag']:<15} {t['description']}\n")
            print(f'\n✅ All the data imported at path: {os.path.join(path, 'tasks.txt')}.')
            break

        elif format == '2':
            with open('tasks.csv', 'w') as csvfile:
                fieldnames = ['id', 'title', 'priority', 'due date', 'done', 'tag', 'description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for t in tasks:
                    writer.writerow(t)
            print(f'\n✅ All the data imported at path: {os.path.join(path, 'tasks.csv')}.') 
            break

        elif format == '0':
            print('\n🛑 - Exporting stopped!')
            break
        else:
            print('\n❌ Error: Enter (1 / 2) or 0 to stop!')
    time.sleep(1)

def intro():
    text = '\n ||  **  WELCOME TO TASK MASTER ** ||\n\nYour ultimate task managment  assistant'
    for i in text:
        print(i, end='', flush=True)
        time.sleep(0.04)
    time.sleep(1)

def ending():
    text = '\n|| ** THANKS FOR USING THIS TASK MANAGER ** ||'
    for i in text:
        print(i, end='', flush=True)
        time.sleep(0.04)
    time.sleep(1)

def guide():
    print('''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
|         QUICK GUIDE         |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
''')
    print('''
1. Add Task
   - Title, description, priority, due date, tag
   - ID is generated automatically

2. View Tasks
   - Shows all tasks in a table

3. Update Task
   - Update task using its ID
   - Title, description, priority, date, tag

4. Delete Task
   - Delete task by ID

5. Filter / Sort
   - Filter by priority or status
   - Sort by title, priority, due date, or status

6. Complete Task
   - Mark task as done or pending

7. Dashboard
   - Total, completed, pending
   - High/medium/low priority
   - Due today / week / overdue

8. Export
   - Export tasks to .txt, .csv, or .json

Tip:
- Enter 0 anytime to cancel an action

============================================
''')
    time.time(1)

def show_all():
    print('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
    print('LET\'S TAKE A START!')
    print('\n1. Add task')
    print('2. Mark as done')
    print('3. Delete task')
    print('4. View all tasks')
    print('5. Update task')
    print('6. Search task')
    print('7. Sort tasks')
    print('8. Statistics dashboard')
    print('9. Export data')
    print('10. Filter by priority')
    print('11. Filter by Tag')
    print('12. Filter by Status')

def main():
    all_actions = [add_task, mark_task, delete_task, view_all_tasks, update_task, search_task, 
    sort_tasks, statistics_screen, export_tasks,  filter_by_priority, filter_by_tag, filter_by_done]

    intro()
    show_all()

    while True:
        try:
            action = int(input('\nEnter (1 - 12): '))

            if action == 0:
                ending()
                break

            all_actions[action - 1]()
            
        except ValueError:
            print('\n❌ Error: Enter an integer!')
        except IndexError:
            print('\n❌ Error: Enter (1 - 12) or 0 to exit!')
            
if __name__ == '__main__':
    main()
#⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋⌈⌉⌊⌋