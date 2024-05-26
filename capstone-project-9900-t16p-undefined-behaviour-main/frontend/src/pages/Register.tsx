import { Box, Button, Container, Heading, VStack } from "@chakra-ui/react";
import { Formik } from "formik";
import { useNavigate } from "react-router-dom";
import FormField from "../components/FormField";
import { apiCall, makeRestaurantName } from "../utils/helpers";
interface RegisterFormValues {
  username: string;
  restaurantName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

function Register() {
  const initialValues: RegisterFormValues = {
    username: "",
    restaurantName: "",
    email: "",
    password: "",
    confirmPassword: "",
  };
  const navigate = useNavigate();
  return (
    <Container>
      <Box borderWidth="1px" borderRadius="lg" padding={"10px"} boxShadow="lg">
        <Heading>Create a Restaurant</Heading>
        <Formik
          initialValues={initialValues}
          onSubmit={(values: RegisterFormValues, actions) => {
            if (values.password !== values.confirmPassword) {
              alert("Passwords do not match");
              return;
            }
            // Check validity
            // Set auth token
            const payload = {
              username: values.username,
              email: values.email,
              password: values.password,
              restaurant_name: values.restaurantName,
            };
            apiCall(`/register`, payload, "POST")
              .then((res: any) => {
                navigate(
                  `/${makeRestaurantName(
                    values.restaurantName
                  )}/staff/manager/dashboard`
                );
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
                  id="restaurantName"
                  label="Enter restaurant name:"
                  required={true}
                />
                <FormField
                  id="email"
                  label="Enter email:"
                  type="email"
                  required={true}
                />
                <FormField
                  id="password"
                  label="Enter password:"
                  type="password"
                  required={true}
                />
                <FormField
                  id="confirmPassword"
                  label="Confirm password:"
                  type="password"
                  required={true}
                />
                <Button type="submit" colorScheme={"teal"}>
                  Register
                </Button>
              </VStack>
            </form>
          )}
        </Formik>
      </Box>
    </Container>
  );
}

export default Register;
