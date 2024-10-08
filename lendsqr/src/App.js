import "./App.css";
import React, { Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import Login from "./containers/Login";
import Dashboard from "./containers/Dashboard";
import UserDetails from "./containers/UserDetails";
import AddUserForm from "./containers/AddUserForm";
import UpdateUserForm from "./containers/UpdateUserForm";
import Signup from "./containers/Signup";
import { Provider } from "react-redux";
import store, { persistor } from "./store";
import { PersistGate } from "redux-persist/integration/react";
import ProtectedRoute from "./components/ProtectedRoute";
import ResetPassword from "./containers/ResetPassword";
import ResetPasswordConfirm from "./containers/ResetPasswordConfirm";
import UserDashboard from "./containers/UserDashboard";
import ProfileForm from "./components/user/ProfileForm";
import AuthUserRoute from "./components/AuthUserRoute";
import Loading from "./components/Loading";

const Login = React.lazy(() => import("./containers/Login"));

function App() {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <BrowserRouter>
          <Suspense fallback={<Loading />}>
            <Routes>
              <Route path="/" exact element={<Login />} />
              <Route path="/signup" exact element={<Signup />} />
              <Route path="/reset-password" exact element={<ResetPassword />} />
              <Route path="/profile-form" exact element={<ProfileForm />} />

              <Route
                path="/password/reset/confirm/:uid/:token"
                exact
                element={<ResetPasswordConfirm />}
              />
              <Route
                path="/user-dashboard"
                element={
                  <AuthUserRoute>
                    <UserDashboard />
                  </AuthUserRoute>
                }
              />
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/user-details"
                element={
                  <ProtectedRoute>
                    <UserDetails />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/add-profile"
                element={
                  <ProtectedRoute>
                    <AddUserForm />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/update-profile"
                element={
                  <ProtectedRoute>
                    <UpdateUserForm />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </PersistGate>
    </Provider>
  );
}

export default App;
