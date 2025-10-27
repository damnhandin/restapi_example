from app.schemas.answer import AnswerRead
from app.schemas.question import QuestionRead, QuestionWithAnswersRead

# Явно перестраиваем модели для разрешения forward refs
QuestionRead.model_rebuild()
AnswerRead.model_rebuild()
QuestionWithAnswersRead.model_rebuild()
