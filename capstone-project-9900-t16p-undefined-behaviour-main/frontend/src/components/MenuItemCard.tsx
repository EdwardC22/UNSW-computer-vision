import { AddIcon, MinusIcon } from "@chakra-ui/icons";
import {
  Button,
  Container,
  Flex,
  Heading,
  IconButton,
  Image,
  Text,
} from "@chakra-ui/react";
import { useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { setOrder } from "../utils/menu";

/// Component used as the full screen card shown to users while ordering a specific item
/// Users can increase or decrease quantity of the item shown before adding it
/// to the basket

const MenuItemCard = () => {
  const { state } = useLocation();
  const item: DItem = state.item;
  const [count, setCount] = useState(1);
  const { restaurantName } = useParams();
  return (
    <Container display={"flex"} flexDir="column" gap="10px" marginBlock="10px">
      {item.image ? (
        <Image
          src={item.image}
          height={350}
          width={"100%"}
          alt={`Image describing restuarant item named ${item.name}`}
        />
      ) : (
        <></>
      )}
      <Heading size={"xl"}>{item.name}</Heading>
      <Heading size={"md"}>Description</Heading>
      <Text>{item.description}</Text>
      <Heading size={"md"}>Ingredients</Heading>
      <Text>{item.ingredients}</Text>
      <Text>${item.cost}</Text>
      <Flex justifyContent={"center"} flexDir="column" gap="10px">
        <Flex justifyContent={"center"} gap="10px">
          <IconButton
            aria-label="Subtract item quantity"
            icon={<MinusIcon />}
            variant="ghost"
            disabled={count <= 1}
            onClick={() => setCount((prev) => prev - 1)}
          />
          <Text fontSize="2xl">{count}</Text>
          <IconButton
            aria-label="Increase item quantity"
            icon={<AddIcon />}
            variant="ghost"
            onClick={() => setCount((prev) => prev + 1)}
          />
        </Flex>
        <Button
          colorScheme={"teal"}
          onClick={() => {
            setOrder(restaurantName, item, count);
            window.history.back();
          }}
        >
          Add for ${(item.cost * count).toFixed(2)}
        </Button>
      </Flex>
    </Container>
  );
};

export default MenuItemCard;
