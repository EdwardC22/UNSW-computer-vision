import { Container, Heading, VStack, Button, Box } from "@chakra-ui/react";
import { Formik } from "formik";
import { useEffect } from "react";
import * as React from "react";
import { useNavigate, useParams } from "react-router-dom";
import FormField from "../components/FormField";
import { apiCall, decodeRestaurantName } from "../utils/helpers";

interface LoginFormValues {
  username: string;
  password: string;
}

function Login() {
  let { restaurantName } = useParams();
  const navigate = useNavigate();

  const initialValues: LoginFormValues = {
    username: "",
    password: "",
  };

  const successfulNav = () => {
    navigate(`/${restaurantName}/staff/manager/dashboard`);
  };

  useEffect(() => {
    const isLoggedIn = () => {
      apiCall(`/${restaurantName}/verifytoken`, {}, "POST")
        .then((res) => successfulNav())
        .catch((_) => console.log("Invalid token, please log in normally"));
    };
    isLoggedIn();
  }, [restaurantName]);

  return (
    <Container>
      <Box borderWidth="1px" borderRadius="lg" padding={"10px"} boxShadow="lg">
        <Heading>{decodeRestaurantName(restaurantName)} Manager Login</Heading>
        <Formik
          initialValues={initialValues}
          onSubmit={(values: LoginFormValues, actions) => {
            // Check validity
            // Set auth token
            apiCall(
              `/${restaurantName}/login`,
              {
                username: values.username,
                password: values.password,
              },
              "POST"
            )
              .then((res: any) => {
                successfulNav();
              })
              .catch((err) => alert(err.error));
          }}
        >
          {({ handleSubmit, errors, touched }) => (
            <form onSubmit={handleSubmit}>
              <VStack>
                <FormField
                  id="username"
                  label="Enter username: "
                  required={true}
                />
                <FormField
                  id="password"
                  label="Enter password:"
                  type="password"
                  required={true}
                />
                <Button type="submit" colorScheme={"teal"}>
                  Login
                </Button>
              </VStack>
            </form>
          )}
        </Formik>
      </Box>
    </Container>
  );
}

export default Login;
