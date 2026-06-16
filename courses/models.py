from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """Model representing a course in the online school."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Model representing a lesson within a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    """Model representing a question in an exam."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    points = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question_text

    def get_choices(self):
        """Return all choices for this question."""
        return self.choices.all()


class Choice(models.Model):
    """Model representing a choice/answer option for a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    """Model representing a student's exam submission."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

    def calculate_score(self):
        """Calculate the score based on selected choices."""
        submission_choices = SubmissionChoice.objects.filter(submission=self)
        correct_answers = 0

        for sub_choice in submission_choices:
            if sub_choice.choice.is_correct:
                correct_answers += 1

        self.score = correct_answers
        self.total_points = self.lesson.questions.count()
        self.save()
        return correct_answers


class SubmissionChoice(models.Model):
    """Model representing a selected choice in a submission."""
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='selected_choices')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Submission Choice'
        verbose_name_plural = 'Submission Choices'

    def __str__(self):
        return f"{self.submission.user.username} selected {self.choice.choice_text}"
