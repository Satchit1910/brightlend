from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .tasks import calculate_and_save_credit_score
from .utils import calculate_credit_score

@api_view(['POST'])
def register_user(request):

    user_id = request.data.get('user_id')
    credit_score = calculate_credit_score(user_id)

    request.data['credit_score'] = credit_score

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        # Save the user's record without credit score
        user = serializer.save()

        # Trigger the Celery task to calculate and save credit score asynchronously
        # user_id = user.user_id
        # calculate_and_save_credit_score.delay(user_id)

        response_data = {
            'id': user.user_id,
            'message': 'User registered successfully.'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)