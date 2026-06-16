from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Question, Choice, Submission, SubmissionChoice


def index(request):
    """Home page view displaying all courses."""
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/index.html', {'courses': courses})


class CourseListView(generic.ListView):
    """Generic list view for courses."""
    model = Course
    template_name = 'courses/index.html'
    context_object_name = 'courses'
    ordering = ['-created_at']


class CourseDetailView(generic.DetailView):
    """Generic detail view for course details with lessons."""
    model = Course
    template_name = 'courses/course_details_bootstrap.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lessons.all().order_by('order')
        return context


def lesson_detail(request, course_id, lesson_id):
    """View for displaying a specific lesson."""
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson
    })


@login_required
def submit(request, course_id):
    """
    View function for submitting exam answers.
    Displays the exam form and handles submission.
    """
    course = get_object_or_404(Course, pk=course_id)
    # Get all questions for lessons in this course
    questions = Question.objects.filter(lesson__course=course)
    
    # We need a Lesson object to save in the Submission.
    # Let's get the first lesson of the course, or create one if none exist.
    lesson = course.lessons.first()
    if not lesson:
        lesson = Lesson.objects.create(course=course, title="Course Exam", content="Exam content")

    if request.method == 'POST':
        # Retrieve enrollment if exists
        from .models import Enrollment
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        
        submission = Submission.objects.create(
            user=request.user,
            lesson=lesson,
            enrollment=enrollment
        )

        total_correct = 0

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                choice = get_object_or_404(Choice, pk=selected_choice_id)
                from .models import SubmissionChoice
                SubmissionChoice.objects.create(
                    submission=submission,
                    choice=choice
                )
                if choice.is_correct:
                    total_correct += 1

        submission.score = total_correct
        submission.total_points = questions.count()
        if submission.total_points > 0:
            submission.grade = (total_correct / submission.total_points) * 100
        else:
            submission.grade = 0.0
        submission.save()

        # Update enrollment grade if this is higher
        if enrollment:
            if submission.grade > enrollment.grade:
                enrollment.grade = submission.grade
                enrollment.save()

        return redirect('courses:show_exam_result', course_id=course.id, submission_id=submission.id)

    return render(request, 'courses/submit.html', {
        'lesson': lesson,
        'questions': questions,
    })


@login_required
def show_exam_result(request, course_id, submission_id):
    """
    View function for displaying exam results.
    Shows the score, correct answers, and feedback.
    """
    submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
    course = get_object_or_404(Course, pk=course_id)
    lesson = submission.lesson

    from .models import SubmissionChoice
    submission_choices = SubmissionChoice.objects.filter(submission=submission)

    questions_with_results = []
    # Get all questions for the course
    questions = Question.objects.filter(lesson__course=course)
    for question in questions:
        selected_choice = submission_choices.filter(choice__question=question).first()
        correct_choice = question.choices.filter(is_correct=True).first()

        questions_with_results.append({
            'question': question,
            'selected_choice': selected_choice.choice if selected_choice else None,
            'correct_choice': correct_choice,
            'is_correct': selected_choice and selected_choice.choice.is_correct if selected_choice else False
        })

    percentage = (submission.score / submission.total_points * 100) if submission.total_points > 0 else 0
    is_passed = submission.is_get_score()


    return render(request, 'courses/exam_result.html', {
        'submission': submission,
        'lesson': lesson,
        'questions_with_results': questions_with_results,
        'percentage': percentage,
        'is_passed': is_passed,
    })



@login_required
def my_submissions(request):
    """View for displaying user's submission history."""
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'courses/my_submissions.html', {
        'submissions': submissions
    })
