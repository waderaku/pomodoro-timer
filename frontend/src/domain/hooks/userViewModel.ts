import {
  AouthToken,
  isSignInAreaFlag,
  isUserSignInFlag,
  UserData,
} from "../model";
import { registerUserAPI, signInUserAPI } from "backendApi";
import { atom, selector, useRecoilState, useRecoilValue } from "recoil";
import { ChangeEvent } from "react";

export const useUserViewModel = () => {
  const [userData, setUserData] = useRecoilState(userDataState);
  const [token, setToken] = useRecoilState(aouthTokenState);
  const [isSignIn, setIsSignIn] = useRecoilState(isSignInAreaState);
  const isUserSignIn = useRecoilValue(isUserSignInSelector);

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
    isUserSignIn,
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

const aouthTokenState = atom<AouthToken>({
  key: "aouthToken",
  default: "",
});

const isSignInAreaState = atom<isSignInAreaFlag>({
  key: "isSignIn",
  default: true,
});

const isUserSignInSelector = selector<isUserSignInFlag>({
  key: "isUserSignIn",
  get: async ({ get }) => {
    console.log(get(aouthTokenState));
    return Boolean(get(aouthTokenState));
  },
});
