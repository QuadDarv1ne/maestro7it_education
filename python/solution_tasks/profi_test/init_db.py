from app import create_app, db
from app.models import TestQuestion

def init_questions():
    """Initialize database with test questions"""
    app = create_app()
    
    with app.app_context():
        # Clear existing questions
        TestQuestion.query.delete()
        
        # Klimov methodology questions
        klimov_questions = [
            {
                'methodology': 'klimov',
                'question_number': 1,
                'text': 'Предпочитаю работать с техникой и механизмами',
                'category': 'Человек-техника'
            },
            {
                'methodology': 'klimov',
                'question_number': 2,
                'text': 'Люблю общаться с людьми и помогать им',
                'category': 'Человек-человек'
            },
            {
                'methodology': 'klimov',
                'question_number': 3,
                'text': 'Интересуюсь природой и живыми организмами',
                'category': 'Человек-природа'
            },
            {
                'methodology': 'klimov',
                'question_number': 4,
                'text': 'Предпочитаю работать с информацией и данными',
                'category': 'Человек-знаковая система'
            },
            {
                'methodology': 'klimov',
                'question_number': 5,
                'text': 'Увлекаюсь творчеством и художественными занятиями',
                'category': 'Человек-художественный образ'
            },
            {
                'methodology': 'klimov',
                'question_number': 6,
                'text': 'Люблю ремонтировать и настраивать оборудование',
                'category': 'Человек-техника'
            },
            {
                'methodology': 'klimov',
                'question_number': 7,
                'text': 'Предпочитаю работать в команде',
                'category': 'Человек-человек'
            },
            {
                'methodology': 'klimov',
                'question_number': 8,
                'text': 'Интересуюсь экологией и охраной окружающей среды',
                'category': 'Человек-природа'
            },
            {
                'methodology': 'klimov',
                'question_number': 9,
                'text': 'Люблю анализировать информацию и решать логические задачи',
                'category': 'Человек-знаковая система'
            },
            {
                'methodology': 'klimov',
                'question_number': 10,
                'text': 'Увлекаюсь дизайном и визуальным творчеством',
                'category': 'Человек-художественный образ'
            },
            {
                'methodology': 'klimov',
                'question_number': 11,
                'text': 'Предпочитаю практическую работу с инструментами',
                'category': 'Человек-техника'
            },
            {
                'methodology': 'klimov',
                'question_number': 12,
                'text': 'Люблю обучать и воспитывать других',
                'category': 'Человек-человек'
            },
            {
                'methodology': 'klimov',
                'question_number': 13,
                'text': 'Интересуюсь биологией и медициной',
                'category': 'Человек-природа'
            },
            {
                'methodology': 'klimov',
                'question_number': 14,
                'text': 'Предпочитаю работу с компьютерами и программами',
                'category': 'Человек-знаковая система'
            },
            {
                'methodology': 'klimov',
                'question_number': 15,
                'text': 'Увлекаюсь музыкой и表演艺术',
                'category': 'Человек-художественный образ'
            },
            {
                'methodology': 'klimov',
                'question_number': 16,
                'text': 'Люблю строить и проектировать',
                'category': 'Человек-техника'
            },
            {
                'methodology': 'klimov',
                'question_number': 17,
                'text': 'Предпочитаю социальную работу',
                'category': 'Человек-человек'
            },
            {
                'methodology': 'klimov',
                'question_number': 18,
                'text': 'Интересуюсь сельским хозяйством и животноводством',
                'category': 'Человек-природа'
            },
            {
                'methodology': 'klimov',
                'question_number': 19,
                'text': 'Люблю работать с числами и статистикой',
                'category': 'Человек-знаковая система'
            },
            {
                'methodology': 'klimov',
                'question_number': 20,
                'text': 'Увлекаюсь литературой и писательством',
                'category': 'Человек-художественный образ'
            }
        ]
        
        # Add questions to database
        for q_data in klimov_questions:
            question = TestQuestion(**q_data)
            db.session.add(question)
        
        db.session.commit()
        print(f"Successfully added {len(klimov_questions)} questions to database")

if __name__ == '__main__':
    init_questions()