# Overview
The Login component is a functional component that handles user login functionality. It utilizes React Hooks for state
management, React Router for navigation, and React Toastify for notifications.

## Variables
### State Variables

- **loading**: A boolean indicating whether the login request is in progress.
- **formData**: An object containing user input data, including email, password, and marketing acceptance.

## Imported Variables

- **`useState`**: A React Hook for state management.
- **`Link`**: A React Router component for navigation.
- **`useNavigate`**: A React Router hook for navigation.
- **`toast`**: A React Toastify component for notifications.
- **`apiRequest`**: A custom API request function.
- **`jwtDecode`**: A function to decode JSON Web Tokens.

## Functions

- **handleChange**  
  Handles changes to form input fields. Updates the `formData` state variable accordingly.

```javascript
const handleChange = (event) => {
  const { name, value } = event.target;
  setFormData({ ...formData, [name]: value });
};
```

- **handleSubmit**  
  Handles form submission. Sends a login request to the API, navigates to the homepage upon success, and displays
  notifications accordingly.

```javascript
const handleSubmit = async (event) => {
  event.preventDefault();
  setLoading(true);

  try {
    const response = await apiRequest('/auth/login', 'POST', formData);
    const token = response.data.token;
    localStorage.setItem('token', token);
    const decodedToken = jwtDecode(token);
    toast.success('Login successful!');
    navigate('/homepage');
  } catch (error) {
    toast.error('Login failed!');
  } finally {
    setLoading(false);
  }
};
```

Conditional Rendering

- **Disabled Button**  
  Disables the login button when the login request is in progress.

```javascript
<button type="submit" disabled={loading}>
  Login
</button>
```

- **Disabled Link**  
  Disables the register link when the login request is in progress.

```javascript
<Link to="/register" disabled={loading}>
  Register
</Link>
```

API Request

- **Endpoint**: `/auth/login`
- **Method**: `POST`
- **Data**: Username (email) and password

Token Management

- **Storage**: Local storage
- **Token**: JSON Web Token (JWT) received from API
- **Decoded Token**: Decoded JWT containing user data

Navigation

- **Homepage**: Navigates to the homepage upon successful login

Notifications

- **Success Toast**: Displays a success notification upon successful login
- **Error Toast**: Displays an error notification upon failed login