import {
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  USER_LOADED_SUCCESS,
  USER_LOADED_FAIL,
  AUTHENTICATION_SUCCESS,
  AUTHENTICATION_FAIL,
  LOGOUT,
  PASSWORD_RESET_SUCCESS,
  PASSWORD_RESET_FAIL,
  PASSWORD_RESET_CONFIRM_SUCCESS,
  PASSWORD_RESET_CONFIRM_FAIL,
  SIGNUP_SUCCESS,
  SIGNUP_FAIL,
  UPDATE_STAFF_STATUS_FAIL,
  UPDATE_STAFF_STATUS_SUCCESS,
  ADD_USER_TO_PORTFOLIO_SUCCESS,
  ADD_USER_TO_PORTFOLIO_FAIL,
  PORTFOLIO_RETRIVAL_SUCCESS,
  PORTFOLIO_RETRIVAL_FAIL,
  PORTFOLIO_UPDATE_SUCCESS,
  PORTFOLIO_UPDATE_FAIL,
  RESET_DONE,
} from "./types";
import axios from "axios";

const LOGIN_URL = "/auth/jwt/create/";
const SIGNUP_URL = "/auth/users/";
const VERIFY_URL = "/auth/jwt/verify/";
const LOAD_USER_URL = "/auth/users/me/";
const ADD_PORTFOLIO_URL = "/api/add-staff-portfolio/";
const UPDATE_PORTFOLIO_URL = "/api/users/";
const STAFF_STATUS_URL = "/api/get_staff_status/";
const RESET_PASSWORD_URL = "/auth/users/reset_password/";
const PASSWORD_RESET_CONFIRM_URL = "/auth/users/reset_password_confirm/";

export const reset = () => async (dispatch) => {
  dispatch({
    type: RESET_DONE,
  });
};

export const checkIsAuthenticated = () => async (dispatch) => {
  if (localStorage.getItem("access")) {
    const config = {
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("access")}`,
        Accept: "application/json",
      },
    };

    const body = JSON.stringify({ token: localStorage.getItem("access") });

    try {
      const res = await axios.post(VERIFY_URL, body, config);
      if (res.data.code !== "token_not_valid") {
        await dispatch({
          type: AUTHENTICATION_SUCCESS,
        });
        return Promise.resolve(res.data);
      } else {
        await dispatch({
          type: AUTHENTICATION_FAIL,
        });
        return Promise.resolve(res.data);
      }
    } catch (err) {
      await dispatch({
        type: AUTHENTICATION_FAIL,
      });
    }

    await dispatch({
      type: AUTHENTICATION_SUCCESS,
    });
  } else {
    await dispatch({
      type: AUTHENTICATION_FAIL,
    });
  }
};

export const load_user = () => async (dispatch) => {
  if (localStorage.getItem("access")) {
    const config = {
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("access")}`,
        Accept: "application/json",
      },
    };

    try {
      const res = await axios.get(LOAD_USER_URL, config);
      await dispatch({
        type: USER_LOADED_SUCCESS,
        payload: res.data,
      });
      return Promise.resolve(res.data);
    } catch (err) {
      await dispatch({
        type: USER_LOADED_FAIL,
      });
      return Promise.reject(err.message);
    }
  } else {
    await dispatch({
      type: USER_LOADED_FAIL,
    });
  }
};

export const login = (email, password) => async (dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = JSON.stringify({ email, password });

  try {
    const res = await axios.post(LOGIN_URL, body, config);

    await dispatch({
      type: LOGIN_SUCCESS,
      payload: res.data,
    });

    await Promise.all([
      dispatch(load_user()),
      dispatch(is_staff(email)),
      dispatch(get_portfolio(email)),
    ]);
    return Promise.resolve(res.data);
  } catch (err) {
    dispatch({
      type: LOGIN_FAIL,
    });
    return Promise.reject(err.message);
  }
};

export const signup =
  (email, first_name, last_name, state, password, re_password) =>
  async (dispatch) => {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    const body = JSON.stringify({
      email,
      first_name,
      last_name,
      state,
      password,
      re_password,
    });

    try {
      const res = await axios.post(SIGNUP_URL, body, config);
      dispatch({
        type: SIGNUP_SUCCESS,
        payload: res.data,
      });
    } catch (err) {
      dispatch({
        type: SIGNUP_FAIL,
      });
    }
  };

export const add_portfolio = (data) => async (dispatch) => {
  const config = {
    headers: {
      "Content-Type": "multipart/form-data",
      Accept: "application/json",
    },
  };

  try {
    await axios.post(ADD_PORTFOLIO_URL, data, config);
    dispatch({
      type: ADD_USER_TO_PORTFOLIO_SUCCESS,
    });
  } catch (err) {
    dispatch({
      type: ADD_USER_TO_PORTFOLIO_FAIL,
    });
  }
};

export const update_portfolio = (data) => async (dispatch) => {
  if (localStorage.getItem("access")) {
    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `JWT ${localStorage.getItem("access")}`,
        Accept: "application/json",
      },
    };

    try {
      await axios.put(UPDATE_PORTFOLIO_URL, data, config);
      dispatch({
        type: PORTFOLIO_UPDATE_SUCCESS,
      });
    } catch (err) {
      dispatch({
        type: PORTFOLIO_UPDATE_FAIL,
      });
    }
  } else {
    dispatch({
      type: PORTFOLIO_UPDATE_FAIL,
    });
  }
};

export const get_portfolio = (email) => async (dispatch) => {
  if (localStorage.getItem("access")) {
    const config = {
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("access")}`,
        Accept: "application/json",
      },
    };

    try {
      const res = await axios.get(
        ADD_PORTFOLIO_URL,
        {
          params: { email: email },
        },
        config
      );
      await dispatch({
        type: PORTFOLIO_RETRIVAL_SUCCESS,
        payload: res.data,
      });
      return Promise.resolve(res.data);
    } catch (err) {
      dispatch({
        type: PORTFOLIO_RETRIVAL_FAIL,
      });
      return Promise.reject(err.message);
    }
  } else {
    dispatch({
      type: PORTFOLIO_RETRIVAL_FAIL,
    });
  }
};

export const is_staff = (email) => async (dispatch) => {
  if (localStorage.getItem("access")) {
    const config = {
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${localStorage.getItem("access")}`,
        Accept: "application/json",
      },
    };

    try {
      const res = await axios.get(
        STAFF_STATUS_URL,
        {
          params: { email: email },
        },
        config
      );
      await dispatch({
        type: UPDATE_STAFF_STATUS_SUCCESS,
        payload: res.data,
      });
      return Promise.resolve(res.data);
    } catch (err) {
      dispatch({
        type: UPDATE_STAFF_STATUS_FAIL,
      });
      return Promise.reject(err.message);
    }
  } else {
    dispatch({
      type: UPDATE_STAFF_STATUS_FAIL,
    });
  }
};

//   export const verify = (uid, token) => async (dispatch) => {
//     const config = {
//       headers: {
//         "Content-Type": "application/json",
//       },
//     };

//     const body = JSON.stringify({ uid, token });

//     try {
//       await axios.post(
//         `${process.env.REACT_APP_GIVEAWAYNOW_API_URL}/auth/users/activation/`,
//         body,
//         config
//       );
//       dispatch({
//         type: ACTIVATION_SUCCESS,
//       });
//     } catch (err) {
//       dispatch({
//         type: ACTIVATION_FAIL,
//       });
//     }
//   };

export const reset_password = (email) => async (dispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = JSON.stringify({ email });

  try {
    await axios.post(RESET_PASSWORD_URL, body, config);
    dispatch({
      type: PASSWORD_RESET_SUCCESS,
    });
  } catch (err) {
    dispatch({
      type: PASSWORD_RESET_FAIL,
    });
  }
};

export const password_reset_confirm =
  (uid, token, new_password, re_new_password) => async (dispatch) => {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    const body = JSON.stringify({ uid, token, new_password, re_new_password });
    try {
      await axios.post(PASSWORD_RESET_CONFIRM_URL, body, config);
      dispatch({
        type: PASSWORD_RESET_CONFIRM_SUCCESS,
      });
    } catch (err) {
      dispatch({
        type: PASSWORD_RESET_CONFIRM_FAIL,
      });
    }
  };

export const logout = () => (dispatch) => {
  dispatch({
    type: LOGOUT,
  });
};
