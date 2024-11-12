from django.shortcuts import render
from django.http import JsonResponse
from .forms import QuizForm
from .utils import *
from django.shortcuts import redirect

def upload_view(request):
    return render(request, 'Quiz_Base/upload.html')

def upload_pdf(request):
    if request.method == 'POST' and 'pdf' in request.FILES:
        try:
            pdf = request.FILES['pdf']
            pdf_text = extract_text_from_pdf(pdf)
            mcq_text = generate_mcqs_with_groq(pdf_text)
            mcqs = parse_mcqs(mcq_text)
            
            if not mcqs:
                messages.error(request, "No valid MCQs could be generated from the uploaded PDF. Please try a different file.")
                return redirect('upload')
                
            request.session['mcqs'] = mcqs
            return JsonResponse({'message': 'Quiz generated successfully', 'redirect': '/quiz/'})
            
        except Exception as e:
            messages.error(request, f"An error occurred while processing the PDF: {str(e)}")
            return redirect('upload')
            
    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.shortcuts import render
from django.http import JsonResponse
from .forms import QuizForm
from .utils import *
from django.template.loader import render_to_string


def quiz_view(request):
    try:
        mcqs = request.session.get('mcqs', [])
        
        if not mcqs:
            messages.error(request, "No valid MCQs could be generated. Please try uploading a different PDF.")
            return redirect('upload')

        if request.method == 'POST':
            form = QuizForm(mcqs=mcqs, data=request.POST)
            if form.is_valid():
                score = 0
                for index, mcq in enumerate(mcqs):
                    user_answer = form.cleaned_data.get(f'question_{index}')
                    if user_answer == mcq['correct_answer']:
                        score += 1
                return JsonResponse({'score': score})

        form = QuizForm(mcqs=mcqs)
        
        questions_data = []
        for i, mcq in enumerate(mcqs):
            questions_data.append({
                'question': mcq['question'],
                'field': form[f'question_{i}']
            })

        return render(request, 'Quiz_Base/quiz.html', {
            'questions_data': questions_data,
        })

    except Exception as e:
        print("Error in quiz_view:", str(e))
        import traceback
        traceback.print_exc()
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('upload')

def submit_quiz(request):
    if request.method == 'POST':
        # Get MCQs from session
        mcqs = request.session.get('mcqs', [])

        # Filter out invalid MCQs
        mcqs = [mcq for mcq in mcqs if mcq['question'] != 'Invalid MCQ format']

        if not mcqs:
            return redirect('upload')  # Redirect to the upload page if there are no MCQs

        score = 0
        for index, mcq in enumerate(mcqs):
            user_answer = request.POST.get(f'q{index}')  # Ensure the input names match the ones in your form
            if user_answer == mcq['correct_answer']:
                score += 1

        return JsonResponse({'score': score})

    return JsonResponse({'error': 'Invalid request method'}, status=400)