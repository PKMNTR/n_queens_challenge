import math
from sqlalchemy import create_engine, Column, Integer, ARRAY, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

class Result(Base):
    __tablename__ = 'result'
    id = Column('id', Integer, primary_key=True)
    board_size = Column('board_size', Integer)
    result = Column('result', ARRAY(Integer))

def can_be_placed(current_solution):
    last_row = len(current_solution) - 1
    for row in range(last_row):
        diff = math.fabs(current_solution[row] - current_solution[last_row])
        if diff == 0 or diff == math.fabs(last_row - row):
            return False
    return True

def solve_n_queens(board_size, row, current_solution, results):
    if row == board_size:
        results.append(current_solution.copy())
    else:
        for column in range(board_size):
            current_solution.append(column)
            if can_be_placed(current_solution):
                solve_n_queens(board_size, row + 1, current_solution, results)
            current_solution.pop()

def n_queens(board_size):
    session = setup_db()
    results = []
    current_solution = []
    solve_n_queens(board_size, 0, current_solution, results)
    save_results(results, board_size, session)
    session.close()
    return len(results)

def setup_db():
    engine = create_engine('postgresql://postgres@localhost/db')
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def save_results(results, board_size, session):
    for result in results:
        result_obj = Result()
        result_obj.board_size = board_size
        result_obj.result = result
        session.add(result_obj)
    session.commit()
