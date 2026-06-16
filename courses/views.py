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
def submit(request, lesson_id):
    """
    View function for submitting exam answers.
    Displays the exam form and handles submission.
    """
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    questions = lesson.questions.all()

    if request.method == 'POST':
        submission = Submission.objects.create(
            user=request.user,
            lesson=lesson
        )

        total_correct = 0

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                choice = get_object_or_404(Choice, pk=selected_choice_id)
                SubmissionChoice.objects.create(
                    submission=submission,
                    choice=choice
                )
                if choice.is_correct:
                    total_correct += 1

        submission.score = total_correct
        submission.total_points = questions.count()
        submission.save()

        return redirect('show_exam_result', submission_id=submission.id)

    return render(request, 'courses/submit.html', {
        'lesson': lesson,
        'questions': questions,
    })


@login_required
def show_exam_result(request, submission_id):
    """
    View function for displaying exam results.
    Shows the score, correct answers, and feedback.
    """
    submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
    lesson = submission.lesson

    submission_choices = SubmissionChoice.objects.filter(submission=submission)

    questions_with_results = []
    for question in lesson.questions.all():
        selected_choice = submission_choices.filter(choice__question=question).first()
        correct_choice = question.choices.filter(is_correct=True).first()

        questions_with_results.append({
            'question': question,
            'selected_choice': selected_choice.choice if selected_choice else None,
            'correct_choice': correct_choice,
            'is_correct': selected_choice and selected_choice.choice.is_correct if selected_choice else False
        })

    percentage = (submission.score / submission.total_points * 100) if submission.total_points > 0 else 0
    is_passed = percentage >= 70

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
