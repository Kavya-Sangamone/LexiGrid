from django.shortcuts import render,redirect
from .forms import UploadFileForm
import hashlib

active_crosswords=[]
def hash_password(password):
    if not isinstance(password, str):
        raise ValueError("Input to md5_hash must be a string.")
    return hashlib.sha256(password.encode()).hexdigest()
def user_landing(request):
    return render(request, 'app1/user_landing.html',{'active_crosswords': active_crosswords})

def home(request):
    return render(request,'app1/login.html')
def superadmin_login(request):
    if request.method == 'POST':
        username = request.POST.get('superadmin_id')
        password = request.POST.get('superadmin_password')
        print("Username:", username)
        
        # Check credentials against super_admin.txt
        text_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/app1/super_admin.txt')
        with open(text_file, 'r') as f:
            for line in f:
                print("Checking line:", line.strip())
                parts = line.strip().split(',')
                print("Parts:", parts)
                print("Expected parts length: 2, Actual parts length:", len(parts))
                print("Username from file:", parts[0] if len(parts) > 0 else "N/A")
                print("Password from file:", parts[1] if len(parts) > 1 else "N/A")
                print("Username from request:", username)
                print("Password from request:", password)
                if len(parts) > 1 and parts[0] == username and parts[1] == password:
                    
                    print("Credentials match")
                    return redirect('super_admin_dashboard')
                else:
                    print("Credentials do not match for line:", line.strip())
        
        # If login fails, render the login page with an error message
        return render(request, 'app1/superAdmin_login.html', {'error': 'Invalid credentials'})

    return render(request,'app1/superAdmin_login.html')
def admin_login(request):

    return render(request,'app1/admin_login.html')
def super_admin_dashboard(request):
    if request.method == 'POST':
        superadmin_id = request.POST.get('superadmin_id')

        superadmin_password = request.POST.get('superadmin_password')
        print("Superadmin ID:", superadmin_id)
        print("Superadmin Password:", superadmin_password)
        
        # Check credentials against super_admin.txt
        text_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/app1/super_admin.txt')
        print("Text file path:", text_file)
        with open(text_file, 'r') as f:
            for line in f:
                print("Checking line:", line.strip())
                parts = line.strip().split(',')
                if len(parts) == 2 and parts[0].strip() == superadmin_id and parts[1].strip() == superadmin_password:
                    print("Credentials match")
                    return render(request, 'app1/SuperAdmin_dashboard.html') # Redirect to add_creator page if credentials match

        # If credentials do not match, show error on dashboard
        return render(request, 'app1/SuperAdmin_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'app1/SuperAdmin_dashboard.html')
from django.contrib import messages  # Add this at the top

def add_creator(request):
    if request.method == 'POST':
        admin_id = request.POST.get('creator_name')
        password = request.POST.get('creator_password')

        print("Admin ID:", admin_id)
        print("Password:", password)
        hashed_password = str(hash_password(password))

        text_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/app1/admin.txt')
        with open(text_file, 'a') as f:
            f.write(f"{admin_id},{hashed_password}\n")

        # Add success message
        messages.success(request, f"Creator added successfully with ID: {admin_id}")
        return redirect('super_admin_dashboard')
    
    return render(request, 'app1/SuperAdmin_dashboard.html')

# def admin_dashboard(request):
#     if request.method == 'POST':
#         admin_id = request.POST.get('admin_id')
#         password = request.POST.get('password')
#         text_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/app1/admin.txt')

          
#         for line in open(text_file, 'r'):
#             parts = line.strip().split(',')
#             if len(parts) >= 2:
#                 file_admin_id = parts[0].strip()
#                 file_password = parts[1].strip()
#                 print(f"Checking: {file_admin_id} == {admin_id} and {file_password} == {password}")
#                 if file_admin_id == admin_id and file_password == password:
#                     return render(request, 'app1/admin_dashboard.html', {'admin_id': admin_id})
        
#     return render(request, 'app1/admin_login.html', {'admin_id': admin_id})
# import os

# import os
# import json
# from django.shortcuts import render, redirect
# from .forms import UploadFileForm

# def upload_file(request):
#     if request.method == 'POST':
        

#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             f = request.FILES['file']

#             # Ensure Questions folder exists
#             os.makedirs('Questions', exist_ok=True)

#             # Save uploaded file
#             file_path = os.path.join('Questions', f.name)
#             with open(file_path, 'wb+') as destination:
#                 for chunk in f.chunks():
#                     destination.write(chunk)

#             # Generate crossword from the uploaded CSV
#             grid, across_clues, down_clues = generate_crossword(csv_path=file_path)
            
#             # Store grid & clues in session so creator() can load them
#             request.session['grid'] = json.dumps(grid)
#             request.session['across_clues'] = json.dumps(across_clues)
#             request.session['down_clues'] = json.dumps(down_clues)
#             admin_id = request.session.get('admin_id')
#             print("admin_id:", admin_id)
#             return redirect('creator', admin_id=admin_id)
#     else:
#         form = UploadFileForm()
#     return render(request, 'app1/admin_dashboard.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import UploadFileForm
import os
import json

def admin_dashboard(request):
    context = {}

    if request.method == 'POST':
        print("POST request received in admin_dashboard")
        # If not logged in, handle login
        if not request.session.get('is_admin_logged_in'):
            admin_id = request.POST.get('admin_id')
            password = hash_password(request.POST.get('password'))
            password=str(password)

            print("admin id",admin_id)
            print(password)
            text_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/app1/admin.txt')
            login_success = False
            for line in open(text_file, 'r'):
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    file_admin_id = parts[0].strip()
                    file_password = parts[1].strip()
                    print(f"Checking: {file_admin_id} == {admin_id} and {file_password} == {password}")
                    if file_admin_id == admin_id and file_password == password:
                        login_success = True
                        break
            if login_success:
                request.session['is_admin_logged_in'] = True
                request.session['admin_id'] = admin_id
                context['form'] = UploadFileForm()
                context['admin_id'] = admin_id
                  # Add to active crosswords
                return render(request, 'app1/admin_dashboard.html', context)
            else:
                context['login_error'] = "Invalid credentials"
                return render(request, 'app1/admin_login.html', context)
        else:
            # Already logged in, handle file upload
            print("Already logged in, handling file upload")
            admin_id = request.POST.get('admin_id') or request.session.get('admin_id')
            password=request.POST.get('password') or request.session.get('password')
            print("Admin ID from POST:", admin_id)
            print("Password from POST:", password)
            form = UploadFileForm(request.POST, request.FILES)
            print("Form data:", request.POST)
            password = hash_password(password) if password else None
            # Always check credentials if provided in POST
            if admin_id and password:
                text_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/app1/admin.txt')
                login_success = False
                for line in open(text_file, 'r'):
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        file_admin_id = parts[0].strip()
                        file_password = parts[1].strip()
                        if file_admin_id == admin_id and file_password == password:
                            login_success = True
                            context['message'] = "Successfully logged in. You can now upload a file."
                            break
                if not login_success:
                    context['login_error'] = "Invalid credentials"
                    return render(request, 'app1/admin_login.html', context)
                request.session['is_admin_logged_in'] = True
                request.session['admin_id'] = admin_id

            if form.is_valid():
                f = request.FILES['file']
                admin_id = request.session['admin_id']
                admin_folder = os.path.join('Questions', admin_id)
                os.makedirs(admin_folder, exist_ok=True)
                file_path = os.path.join(admin_folder, f.name)

                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                
                grid, across_clues, down_clues = generate_crossword(csv_path=file_path)
                active_crosswords.append(f.name)  # Add to active crosswords
                request.session['grid'] = json.dumps(grid)
                request.session['across_clues'] = json.dumps(across_clues)
                request.session['down_clues'] = json.dumps(down_clues)
                return redirect('creator', admin_id=admin_id)
            else:
                context['form'] = form
                context['admin_id'] = request.session.get('admin_id')
                return render(request, 'app1/admin_dashboard.html', context)
    else:
        # GET request
        if request.session.get('is_admin_logged_in'):
            context['form'] = UploadFileForm()
            context['admin_id'] = request.session['admin_id']

            return render(request, 'app1/admin_dashboard.html', context)
        else:
            
            return render(request, 'app1/admin_login.html', context)


# def creator(request):
    # if 'reset' in request.GET:
    #     # Clear crossword session data
    #     request.session.flush()
    #     return redirect('home') 
    # # Check if crossword is already stored in session
    # if 'grid' in request.session and 'across_clues' in request.session and 'down_clues' in request.session:
    #     grid = json.loads(request.session['grid'])
    #     across_clues = json.loads(request.session['across_clues'])
    #     down_clues = json.loads(request.session['down_clues'])
    # else:
        # Generate new crossword
    # grid, across_clues, down_clues = generate_crossword()
    
    # Store in session as JSON strings (since session data must be JSON-serializable)
    # request.session['grid'] = json.dumps(grid)
    # request.session['across_clues'] = json.dumps(across_clues)
    # request.session['down_clues'] = json.dumps(down_clues)
    # clue_numbers = {(clue['row'], clue['col']): clue['num'] for clue in across_clues + down_clues}
    

# Build the indexed list with optional clue numbers
    # indexed_list = [
    #     [
    #         {
    #             'row': i,
    #             'col': j,
    #             'letter': grid[i][j] if grid[i][j]!=" " else None,
    #             'clue_num': clue_numbers.get((i, j), None)
    #         }
    #         for j in range(len(grid))
    #     ]
    #     for i in range(len(grid))
    # ]

    # context = {
    #     'indexed_list': indexed_list,
    #     'across_clues': across_clues,
    #     'down_clues': down_clues,
    # }
    # return render(request, 'app1/creator.html', context)
def creator(request, admin_id):
    if 'grid' in request.session:
        grid = json.loads(request.session['grid'])
        across_clues = json.loads(request.session['across_clues'])
        down_clues = json.loads(request.session['down_clues'])
    else:
        grid, across_clues, down_clues = generate_crossword()

    clue_numbers = {(clue['row'], clue['col']): clue['num'] for clue in across_clues + down_clues}

    indexed_list = [
        [
            {
                'row': i,
                'col': j,
                'letter': grid[i][j] if grid[i][j] != " " else None,
                'clue_num': clue_numbers.get((i, j), None)
            }
            for j in range(len(grid))
        ]
        for i in range(len(grid))
    ]

    context = {
        'indexed_list': indexed_list,
        'across_clues': across_clues,
        'down_clues': down_clues,
        'admin_id': admin_id,   # Pass it to your template if needed
    }
    return render(request, 'app1/creator.html', context)



def user(request):
    # if 'reset' in request.GET:
    #     # Clear crossword session data
    #     request.session.flush()
    #     return redirect('home') 
    # # Check if crossword is already stored in session
    # if 'grid' in request.session and 'across_clues' in request.session and 'down_clues' in request.session:
    #     grid = json.loads(request.session['grid'])
    #     across_clues = json.loads(request.session['across_clues'])
    #     down_clues = json.loads(request.session['down_clues'])
    # else:
        # Generate new crossword
    grid, across_clues, down_clues = generate_crossword()
    # Store in session as JSON strings (since session data must be JSON-serializable)
    # request.session['grid'] = json.dumps(grid)
    # request.session['across_clues'] = json.dumps(across_clues)
    # request.session['down_clues'] = json.dumps(down_clues)
    clue_numbers = {(clue['row'], clue['col']): clue['num'] for clue in across_clues + down_clues}

# Build the indexed list with optional clue numbers
    indexed_list = [
        [
            {
                'row': i,
                'col': j,
                'letter': grid[i][j] if grid[i][j]!=" " else None,
                'clue_num': clue_numbers.get((i, j), None)
            }
            for j in range(len(grid))
        ]
        for i in range(len(grid))
    ]

    context = {
        'indexed_list': indexed_list,
        'across_clues': across_clues,
        'down_clues': down_clues,
    }
    from datetime import datetime

# Generate crossword
    from datetime import datetime
    import os

# Get grid and clues
    grid, across_clues, down_clues = generate_crossword()

    if grid is not None and across_clues is not None and down_clues is not None:
        # Timestamp for filename
        timestamp = datetime.now().strftime("%Y_%m_%d_%H-%M")

        # Directory and filenames
        base_dir = r'E:\LexiGrid\LexiGrid2\Files'
        blank_file = os.path.join(base_dir, f'lexigrid_blank_{timestamp}.txt')
        filled_file = os.path.join(base_dir, f'lexigrid_filled_{timestamp}.txt')
        clue_file = os.path.join(base_dir, f'clue_{timestamp}.txt')  # Already used in generate_crossword

        os.makedirs(base_dir, exist_ok=True)

        # Save blank grid (hide letters with '.')
        with open(blank_file, 'a') as f:
            for row in grid:
                f.write(' '.join('.' if cell.isalpha() else cell for cell in row) + '\n')
            f.write('\n')

        # Save filled grid
        with open(filled_file, 'a') as f:
            for row in grid:
                f.write(' '.join(cell if cell.strip() else ' ' for cell in row) + '\n')
            f.write('\n')

        # Save clues (append to clue.txt)
        with open(clue_file, 'a') as f:
            f.write(f"\n=== Clues for crossword {timestamp} ===\n")
            f.write("Across:\n")
            for clue in across_clues:
                f.write(f"{clue['num']}. {clue['clue']} ({clue['length']})\n")
            f.write("Down:\n")
            for clue in down_clues:
                f.write(f"{clue['num']}. {clue['clue']} ({clue['length']})\n")
            f.write("\n")

    return render(request, 'app1/user.html', context)

import csv
import random
import os
import json


# logger = logging.getLogger(__name__)

GRID_SIZE = 20
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name='space.csv'
csv_path = os.path.join(BASE_DIR,  'Questions',file_name)

# def generate_crossword():
#         # Initialize grid and variables
#         grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
#         placed_words = []
#         fitted_words = []
#         unfitted_words = []
#         clue_number = 1

#         words = []
#         clues = []
#         try:
#             with open(csv_path, 'r') as file:
#                 for line in file:
#                     parts = line.strip().split(',', 1)
#                     if parts and parts[0].strip():
#                         word = parts[0].strip().upper()
#                         if word.isalpha():
#                             words.append(word)
#                             clues.append(parts[1].strip() if len(parts) > 1 else "No clue provided")
#                         else:
#                             unfitted_words.append(word)
#         except FileNotFoundError:
#             print("CSV file not found")
#             return None, None, None
#         except csv.Error:
#             print("Invalid CSV format")
#             return None, None, None

#         word_lengths = [len(word) for word in words]
#         avg_length = sum(word_lengths) / len(words) if word_lengths else 1

#         if avg_length < (GRID_SIZE/2):
#             words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=True)
#         else:
#             words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=False)

#         words, clues = zip(*words_with_clues) if words_with_clues else ([], [])

#         def can_place(word, row, col, direction, require_intersection=True):
#             length = len(word)
#             if row < 0 or col < 0:
#                 return False
#             if direction == "across" and col + length > GRID_SIZE:
#                 return False
#             if direction == "down" and row + length > GRID_SIZE:
#                 return False

#             intersections = 0
#             for i in range(length):
#                 r = row + (i if direction == "down" else 0)
#                 c = col + (i if direction == "across" else 0)
#                 if r >= GRID_SIZE or c >= GRID_SIZE:
#                     return False
#                 existing = grid[r][c]
#                 if existing != " ":
#                     if existing != word[i]:
#                         return False
#                     intersections += 1
#                 else:
#                     if direction == "across":
#                         if (row > 0 and grid[row - 1][c] != " ") or (row < GRID_SIZE - 1 and grid[row + 1][c] != " "):
#                             return False
#                     elif direction == "down":
#                         if (col > 0 and grid[r][col - 1] != " ") or (col < GRID_SIZE - 1 and grid[r][col + 1] != " "):
#                             return False

#             if direction == "across":
#                 if (col > 0 and grid[row][col - 1] != " ") or (col + length < GRID_SIZE and grid[row][col + length] != " "):
#                     return False
#             else:
#                 if (row > 0 and grid[row - 1][col] != " ") or (row + length < GRID_SIZE and grid[row + length][col] != " "):
#                     return False

#             if require_intersection and placed_words:
#                 return intersections >= 1
#             return True

#         def place_word(word, row, col, direction, clue_number, clue):
#             for i in range(len(word)):
#                 r = row + (i if direction == "down" else 0)
#                 c = col + (i if direction == "across" else 0)
#                 grid[r][c] = word[i]

#             placed_words.append((word, row, col, direction, clue_number, clue))
#             fitted_words.append(word)

#         def find_best_location(word):
#             placed_words_shuffled = placed_words[:]
#             random.shuffle(placed_words_shuffled)

#             if not placed_words:
#                 for row in range(GRID_SIZE):
#                     for col in range(GRID_SIZE):
#                         for direction in ["across", "down"]:
#                             if can_place(word, row, col, direction, require_intersection=False):
#                                 return row, col, direction
#                 return None

#             for existing_word, erow, ecol, edir, _, _ in placed_words_shuffled:
#                 for i, char in enumerate(existing_word):
#                     for letter in word:
#                         if letter == char:
#                             base_row = erow + (i if edir == "down" else 0)
#                             base_col = ecol + (i if edir == "across" else 0)
#                             for new_dir in ["across", "down"]:
#                                 if new_dir != edir:
#                                     word_idx = word.index(letter)
#                                     start_row = base_row - (word_idx if new_dir == "down" else 0)
#                                     start_col = base_col - (word_idx if new_dir == "across" else 0)
#                                     if start_row >= 0 and start_col >= 0:
#                                         if can_place(word, start_row, start_col, new_dir):
#                                             return start_row, start_col, new_dir

#             for row in range(GRID_SIZE):
#                 for col in range(GRID_SIZE):
#                     for direction in ["across", "down"]:
#                         if can_place(word, row, col, direction, require_intersection=False):
#                             return row, col, direction
#             return None

#         for idx, (word, clue) in enumerate(zip(words, clues)):
#             if len(word) > GRID_SIZE:
#                 unfitted_words.append(word)
#                 continue
#             location = find_best_location(word)
#             if location:
#                 row, col, direction = location
#                 place_word(word, row, col, direction, clue_number, clue)
#                 clue_number += 1
#             else:
#                 unfitted_words.append(word)

#         across_clues = []
#         down_clues = []

#         for word, row, col, direction, num, clue in sorted(placed_words, key=lambda x: x[4]):
#             entry = {
#                 'num': num,
#                 'clue': clue,
#                 'answer': word,
#                 'row': row,
#                 'col': col,
#                 'length':len(word)
#             }
#             if direction == "across":
#                 across_clues.append(entry)
#             else:
#                 down_clues.append(entry)
        
        

#         return grid, across_clues, down_clues
    
def generate_crossword(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(BASE_DIR, 'Questions', file_name)

    grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    placed_words = []
    fitted_words = []
    unfitted_words = []
    clue_number = 1

    words = []
    clues = []
    try:
        with open(csv_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',', 1)
                if parts and parts[0].strip():
                    word = parts[0].strip().upper()
                    if word.isalpha():
                        words.append(word)
                        clues.append(parts[1].strip() if len(parts) > 1 else "No clue provided")
                    else:
                        unfitted_words.append(word)
    except FileNotFoundError:
        print("CSV file not found:", csv_path)
        return None, None, None
    except csv.Error:
        print("Invalid CSV format:", csv_path)
        return None, None, None

    word_lengths = [len(word) for word in words]
    avg_length = sum(word_lengths) / len(words) if word_lengths else 1

    if avg_length < (GRID_SIZE/2):
        words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=True)
    else:
        words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=False)

    words, clues = zip(*words_with_clues) if words_with_clues else ([], [])

    def can_place(word, row, col, direction, require_intersection=True):
        length = len(word)
        if row < 0 or col < 0:
            return False
        if direction == "across" and col + length > GRID_SIZE:
            return False
        if direction == "down" and row + length > GRID_SIZE:
            return False

        intersections = 0
        for i in range(length):
            r = row + (i if direction == "down" else 0)
            c = col + (i if direction == "across" else 0)
            if r >= GRID_SIZE or c >= GRID_SIZE:
                return False
            existing = grid[r][c]
            if existing != " ":
                if existing != word[i]:
                    return False
                intersections += 1
            else:
                if direction == "across":
                    if (row > 0 and grid[row - 1][c] != " ") or (row < GRID_SIZE - 1 and grid[row + 1][c] != " "):
                        return False
                elif direction == "down":
                    if (col > 0 and grid[r][col - 1] != " ") or (col < GRID_SIZE - 1 and grid[r][col + 1] != " "):
                        return False

        if direction == "across":
            if (col > 0 and grid[row][col - 1] != " ") or (col + length < GRID_SIZE and grid[row][col + length] != " "):
                return False
        else:
            if (row > 0 and grid[row - 1][col] != " ") or (row + length < GRID_SIZE and grid[row + length][col] != " "):
                return False

        if require_intersection and placed_words:
            return intersections >= 1
        return True

    def place_word(word, row, col, direction, clue_number, clue):
        for i in range(len(word)):
            r = row + (i if direction == "down" else 0)
            c = col + (i if direction == "across" else 0)
            grid[r][c] = word[i]

        placed_words.append((word, row, col, direction, clue_number, clue))
        fitted_words.append(word)

    def find_best_location(word):
        placed_words_shuffled = placed_words[:]
        random.shuffle(placed_words_shuffled)

        if not placed_words:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    for direction in ["across", "down"]:
                        if can_place(word, row, col, direction, require_intersection=False):
                            return row, col, direction
            return None

        for existing_word, erow, ecol, edir, _, _ in placed_words_shuffled:
            for i, char in enumerate(existing_word):
                for letter in word:
                    if letter == char:
                        base_row = erow + (i if edir == "down" else 0)
                        base_col = ecol + (i if edir == "across" else 0)
                        for new_dir in ["across", "down"]:
                            if new_dir != edir:
                                word_idx = word.index(letter)
                                start_row = base_row - (word_idx if new_dir == "down" else 0)
                                start_col = base_col - (word_idx if new_dir == "across" else 0)
                                if start_row >= 0 and start_col >= 0:
                                    if can_place(word, start_row, start_col, new_dir):
                                        return start_row, start_col, new_dir

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                for direction in ["across", "down"]:
                    if can_place(word, row, col, direction, require_intersection=False):
                        return row, col, direction
        return None

    for idx, (word, clue) in enumerate(zip(words, clues)):
        if len(word) > GRID_SIZE:
            unfitted_words.append(word)
            continue
        location = find_best_location(word)
        if location:
            row, col, direction = location
            place_word(word, row, col, direction, clue_number, clue)
            clue_number += 1
        else:
            unfitted_words.append(word)

    across_clues = []
    down_clues = []

    for word, row, col, direction, num, clue in sorted(placed_words, key=lambda x: x[4]):
        entry = {
            'num': num,
            'clue': clue,
            'answer': word,
            'row': row,
            'col': col,
            'length': len(word)
        }
        if direction == "across":
            across_clues.append(entry)
        else:
            down_clues.append(entry)
    return grid, across_clues, down_clues