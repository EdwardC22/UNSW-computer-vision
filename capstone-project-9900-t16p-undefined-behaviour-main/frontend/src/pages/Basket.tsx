import { AddIcon, MinusIcon } from "@chakra-ui/icons";
import {
  Button,
  Container,
  Flex,
  IconButton,
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { apiCall } from "../utils/helpers";
import { getOrder, setOrder } from "../utils/menu";

/// Customer basket stores current items that have not yet been ordered

interface BasketItemsProps {
  name: string;
  cost: number;
  quantity: number;
  id: number;
  update: any;
}

const BasketItem = ({ name, cost, quantity, id, update }: BasketItemsProps) => {
  const { restaurantName } = useParams();
  return (
    <tr>
      <Td>{name.length > 12 ? `${name.slice(0, 10)}...` : name}</Td>
      <Td>
        <Flex justifyContent={"center"} gap="10px" alignItems={"center"}>
          <IconButton
            aria-label="Subtract item quantity"
            icon={<MinusIcon />}
            variant="ghost"
            onClick={() => {
              setOrder(restaurantName, { name, cost, id }, -1);
              update();
            }}
          />
          <Text fontSize="xl">{quantity}</Text>
          <IconButton
            aria-label="Increase item quantity"
            icon={<AddIcon />}
            variant="ghost"
            onClick={() => {
              setOrder(restaurantName, { name, cost, id }, 1);
              update();
            }}
          />
        </Flex>
      </Td>
      <Td>${cost}</Td>
    </tr>
  );
};

interface orderType {
  itemID: number;
  quantity: number;
}

const Basket = () => {
  const navigate = useNavigate();
  const { restaurantName, tableNumber } = useParams();

  let restName = "";
  if (restaurantName === undefined || !tableNumber === undefined) {
    navigate("/*");
  }
  if (restaurantName !== undefined) {
    restName = restaurantName;
  }
  useEffect(() => {
    async function validateTableNumber() {
      apiCall(`/${restaurantName}/tables`, {}, "GET")
        .then((res: any) => {
          const table: string = tableNumber === undefined ? "" : tableNumber;
          if (tableNumber === "") {
            navigate(`/${restaurantName}/order`);
          }
          const tableNum = parseInt(table);
          if (tableNum < 1 || tableNum > res.tables) {
            navigate(`/${restaurantName}/order`);
          }
        })
        .catch((err) => console.log(err));
    }
    validateTableNumber();
  }, [navigate, restaurantName, tableNumber]);

  const updateOrder = () => {
    setOrder(getOrder(restName));
  };

  const [order, setOrder] = useState(getOrder(restName));
  async function submitOrder() {
    let payload = order.map((itemTuple: [BasketItemsProps, number]) => {
      let newValue: orderType = {
        itemID: itemTuple[0].id,
        quantity: itemTuple[1],
      };
      return newValue;
    });
    try {
      await apiCall(`/${restaurantName}/${tableNumber}`, payload, "POST");
      localStorage.setItem(restName, JSON.stringify([]));
      updateOrder();
      navigate(`/${restaurantName}/order/${tableNumber}/progress`);
    } catch (err: any) {
      alert(`Error submitting order: ${err.error}`);
    }
  }
  const [orderCost, setOrderCost] = useState(0);
  useEffect(() => {
    // Anytime order changes calculate total cost
    function calculateCost() {
      const initValue = 0;
      let cost = order.reduce(
        (previous: number, current: [BasketItemsProps, number]) =>
          previous + current[0].cost * current[1],
        initValue
      );
      setOrderCost(cost);
    }
    calculateCost();
  }, [order]);
  return (
    <Container padding={0}>
      {order.length > 0 ? (
        <>
          <TableContainer>
            <Table size="sm">
              <Thead>
                <tr>
                  <Th>Name</Th>
                  <Th>Quantity</Th>
                  <Th>Cost($)</Th>
                </tr>
              </Thead>
              <Tbody>
                {order.map(
                  (itemTuple: [BasketItemsProps, number], idx: number) => (
                    <BasketItem
                      key={idx}
                      name={itemTuple[0].name}
                      cost={itemTuple[0].cost}
                      quantity={itemTuple[1]}
                      id={itemTuple[0].id}
                      update={updateOrder}
                    />
                  )
                )}
                <tr>
                  <Td fontSize="xl">Total cost:</Td>
                  <Td></Td>
                  <Td fontSize="xl">${orderCost.toFixed(2)}</Td>
                </tr>
              </Tbody>
            </Table>
          </TableContainer>
          <Flex justifyContent={"flex-end"} marginBlock={"10px"}>
            <Button onClick={submitOrder} colorScheme={"teal"}>
              Place order
            </Button>
          </Flex>
        </>
      ) : (
        <Text marginTop={"10px"}>Please add an item to your order</Text>
      )}
    </Container>
  );
};

export default Basket;
