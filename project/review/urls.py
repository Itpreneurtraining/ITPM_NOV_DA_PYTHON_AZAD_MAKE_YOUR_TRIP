from django.urls import path
from . import views

urlpatterns = [
    # ✅ Route to write a review (requires booking_id)
    path('write_review/', views.write_review, name='write_review'),

    # ✅ Route to thank-you page after review submission (booking_id passed for context)
    path('review_submitted/', views.review_submitted, name='review_submitted'),

    # ✅ Route to view all reviews
    path('all_reviews/', views.all_reviews, name='all_reviews'),
    path('like/<int:review_id>/', views.like_review, name='like_review'),
    path('comment/<int:review_id>/', views.comment_on_review, name='comment_on_review'),
]