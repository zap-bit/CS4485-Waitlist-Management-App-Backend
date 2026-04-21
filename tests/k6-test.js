import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 }, // Ramp up to 10 users over 30 seconds
    { duration: '1m', target: 10 }, // Stay at 10 users for 1 minute
    { duration: '30s', target: 0 }, // Ramp down to 0 users over 30 seconds
  ],
};
const supabaseToken = ''; // put the supabase key here bc k6 cant use dotenv. make sure to delete it before pushing or anything tho
export default function () {
  const url = 'http://localhost:8000/'; // Replace the end with any of the endpoints to test them (i put them in routes.txt)
  const payload = JSON.stringify({
    key: 'value', // Replace with your request payload
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${supabaseToken}`, // Use Supabase token from .env
    },
  };

  const res = http.post(url, payload, params);

  // it will say we fail all calls, but that is just because we are not sending a status code on succsess, and only sending one on errors.
  check(res, {
    'is status 200': (r) => r.status === 200,
  });

  sleep(1); // Simulate user wait time
}