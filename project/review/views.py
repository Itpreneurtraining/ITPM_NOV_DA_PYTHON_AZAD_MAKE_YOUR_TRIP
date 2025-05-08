from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Review, ReviewLike, ReviewComment
from .forms import ReviewForm, ReviewCommentForm
from booking.models import TravelBooking


def write_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_submitted')
    else:
        form = ReviewForm()

    return render(request, 'review/write_review.html', {'form': form})


def review_submitted(request):
    review = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'review/review_submitted.html', {'review': review})


def all_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')

    # Get current session key
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    # Loop and attach is_liked property
    for review in reviews:
        if request.user.is_authenticated:
            is_liked = ReviewLike.objects.filter(review=review, user=request.user).exists()
        else:
            is_liked = ReviewLike.objects.filter(review=review, session_key=session_key).exists()
        review.is_liked = is_liked  # dynamically attach attribute

    return render(request, 'review/all_reviews.html', {'reviews': reviews})

def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    like, created = ReviewLike.objects.get_or_create(
        review=review,
        user=request.user if request.user.is_authenticated else None,
        session_key=session_key
    )

    if not created:
        like.delete()  # Toggle like off

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('all_reviews')))


def comment_on_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review

            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.name = form.cleaned_data.get('name')

            comment.save()
            return redirect('all_reviews')
    else:
        form = ReviewCommentForm()

    return render(request, 'review/comment_form.html', {'form': form, 'review': review})