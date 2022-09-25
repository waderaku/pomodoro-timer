import { registerUserAPI, signInUserAPI } from "backendApi";
import { authTokenState } from "domain/hooks/core";
import { IsSignInArea, OnSignIn, UserData } from "domain/model";
import { ChangeEvent } from "react";
import { atom, selector, useRecoilState, useRecoilValue } from "recoil";

export const useUserViewModel = () => {
  const [userData, setUserData] = useRecoilState(userDataState);
  const [token, setToken] = useRecoilState(authTokenState);
  const [isSignIn, setIsSignIn] = useRecoilState(isSignInAreaState);
  const onSignIn = useRecoilValue(onSignInSelector);

  const handleUpdateUserId = (
    e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    setUserData({
      ...userData,
      userId: e.target.value,
    });
  };

  const handleUpdatePassword = (
    e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    setUserData({
      ...userData,
      password: e.target.value,
    });
  };

  const resetUserIdAndPassword = () => {
    setUserData({
      userId: "",
      password: "",
    });
  };

  const toSignIn = () => {
    setIsSignIn(!isSignIn);
  };

  const toSignUp = () => {
    resetUserIdAndPassword();
    setIsSignIn(!isSignIn);
  };

  const signInUser = async () => {
    const token = await signInUserAPI(userData);
    setToken(token);
  };

  const signOutUser = () => {
    setToken("");
  };

  const createUser = async () => {
    await registerUserAPI(userData);
    setIsSignIn(!isSignIn);
  };

  return {
    token,
    onSignIn,
    userData,
    isSignIn,
    handleUpdateUserId,
    handleUpdatePassword,
    toSignIn,
    toSignUp,
    createUser,
    signInUser,
    signOutUser,
  };
};

const userDataState = atom<UserData>({
  key: "userData",
  default: {
    userId: "",
    password: "",
  },
});



const isSignInAreaState = atom<IsSignInArea>({
  key: "isSignIn",
  default: true,
});

const onSignInSelector = selector<OnSignIn>({
  key: "isSignedIn",
  get: async ({ get }) => {
    return Boolean(get(authTokenState));
  },
});
