import { Button, Center, Container, Flex, Heading } from "@chakra-ui/react";
import { Link as routerLink, useParams } from "react-router-dom";
import { decodeRestaurantName } from "../utils/helpers";

function StaffPortal() {
  let { restaurantName } = useParams();
  return (
    <Container>
      <Center flexDirection={"column"}>
        <Heading>{decodeRestaurantName(restaurantName)}'s Staff Portal</Heading>
        <Flex justifyContent={"space-between"} width="100%" marginTop="10%">
          <Button colorScheme={"teal"} as={routerLink} to="manager">
            Manager
          </Button>
          <Button colorScheme={"purple"} as={routerLink} to="wait">
            Wait Staff
          </Button>
          <Button colorScheme={"green"} as={routerLink} to="kitchen">
            Kitchen Staff
          </Button>
        </Flex>
      </Center>
    </Container>
  );
}

export default StaffPortal;
