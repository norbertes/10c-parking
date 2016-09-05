from django.http import JsonResponse


def get_parking_data(request):
    with open('../../last_count.txt', 'r') as file:
        line = file.readline(1)
        taken_slots = int(line)

    data = {
        'image_url': '10.0.2.11:8000/static/last_image.jpg',
        'taken_slots': taken_slots
    }
    return JsonResponse(data, safe=True)
