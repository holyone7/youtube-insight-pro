import os
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', None)

def start_checkout(channel_id, unit_amount=5000):
    if not stripe.api_key:
        return f"https://example.com/simulated-checkout?product=YouTubeReport&channel={channel_id}&amount={unit_amount}"
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': f'YouTube Report for {channel_id}'},
                'unit_amount': unit_amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=os.environ.get('SUCCESS_URL', 'https://your-domain.com/success') + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=os.environ.get('CANCEL_URL', 'https://your-domain.com/cancel'),
    )
    return session.url
