import SignInFeild from "./SignInFeild";
import SignUpFeild from "./SignUpFeild";
import { useUserViewModel } from "domain/hooks/userViewModel";

const SignFeild = () => {
  const { isSignIn } = useUserViewModel();

  if (isSignIn) {
    return <SignInFeild />;
  } else {
    return <SignUpFeild />;
  }
};
export default SignFeild;
