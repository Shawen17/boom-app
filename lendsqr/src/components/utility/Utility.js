export const regex =
  "/^(?=.*[a-z])(?=.*[A-Z])(?=.*d)(?=.*[!@#$%^&*])[A-Za-zd!@#$%^&*]{8,30}$/";

export const MEDIA_URL = "https://shawenmedia.s3.amazonaws.com";

export const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func(...args);
    }, delay);
  };
};
