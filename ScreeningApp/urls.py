from django.urls import path
from ScreeningApp  import views

urlpatterns = [
	path('screenings/<screening_uuid>/',views.Screening.as_view(),name='screening'),
	path('screenings/<screening_uuid>/screening-preview/',views.Screening_Preview.as_view(),name='screening_preview'),
	path('screenings/<screening_uuid>/screening-result/',views.Result.as_view(),name='result'),
	path('screenings/<screening_uuid>/screening-result/screening-status/',views.Feedback.as_view(),name='screening-status'),

]
