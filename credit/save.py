

def post(self, request: HttpRequest):
        amount = int(request.POST.get('amount'))
        rate = CURRENT_RATE
        months = int(request.POST.get('months'))
        value = request.POST.get('type')

        i = rate / 12 / 100  # месячная ставка

        context = {
            'amount': amount,
            'rate': rate,
            'months': months,
        }

        action = request.POST.get('action')

        if action == "calculate":
            monthly_payment = amount * ((i * (1 + i) ** months) / ((1 + i) ** months - 1))
            total_payment = monthly_payment * months
            total_interest = total_payment - amount

            context['result'] = {
                'monthly_payment': round(monthly_payment, 2),
                'total_interest': round(total_interest, 2),
                'total_payment': round(total_payment, 2),
                'method': 'Аннуитетный',
            }

            return render(request, 'credit/credit.html', context=context)
     
        if action == 'save':
            monthly_payment = amount * ((i * (1 + i) ** months) / ((1 + i) ** months - 1))
            total_payment = monthly_payment * months
            total_interest = total_payment - amount

            credit = Credit.objects.create(
                user=request.user,
                amount=amount,
                rate=rate,
                months=months,
                monthly_payment=monthly_payment,
                total_payment=total_payment,
                total_interest=total_interest,
            )

        
            #return redirect('home:credit')
        
        return redirect('credit:credit')