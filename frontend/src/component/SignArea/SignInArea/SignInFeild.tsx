import {
  Card,
  CardContent,
  Grid,
  TextField,
  Box,
  CardActions,
  Button,
  Typography,
} from "@mui/material";
import { useUserViewModel } from "domain/hooks/userViewModel";
import { ChangeEvent } from "react";

const SignInFeild = () => {
  const {
    userData,
    handleUpdateUserId,
    handleUpdatePassword,
    toSignUp,
    signInUser,
  } = useUserViewModel();

  return (
    <Grid container justifyContent="center">
      <Grid item xs={8}>
        <Card variant="outlined">
          <CardContent>
            <Grid
              container
              direction="row"
              justifyContent="center"
              alignItems="center"
            >
              <Grid item xs={10}>
                <Box mt={1}>
                  <Typography variant="h4" align="center">
                    ログイン
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={10}>
                <Box mt={1}>
                  <TextField
                    fullWidth
                    id="userId"
                    label="User Id"
                    onChange={(
                      e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
                    ) => handleUpdateUserId(e)}
                    defaultValue={userData.userId}
                    variant="standard"
                  />
                </Box>
              </Grid>
            </Grid>
            <Grid
              container
              direction="row"
              justifyContent="center"
              alignItems="center"
            >
              <Grid item xs={10}>
                <Box mt={1}>
                  <TextField
                    fullWidth
                    id="password"
                    label="Password"
                    type="password"
                    onChange={(
                      e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
                    ) => handleUpdatePassword(e)}
                    defaultValue={userData.userId}
                    variant="standard"
                  />
                </Box>
              </Grid>
            </Grid>
          </CardContent>
          <CardActions>
            <Grid
              container
              direction="row"
              justifyContent="space-evenly"
              alignItems="center"
            >
              <Button size="small" onClick={toSignUp}>
                To SignUp Menu
              </Button>
              <Button size="small" onClick={signInUser}>
                Sign in
              </Button>
            </Grid>
          </CardActions>
        </Card>
      </Grid>
    </Grid>
  );
};
export default SignInFeild;
