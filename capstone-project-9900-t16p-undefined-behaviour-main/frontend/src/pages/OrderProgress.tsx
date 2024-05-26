import {
  Button,
  Center,
  Container,
  Flex,
  Spinner,
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

interface OrderType {
  cost: number;
  name: string;
  quantity: number;
  status: string;
}

const OrderProgress = () => {
  const { restaurantName, tableNumber } = useParams();
  const [data, setData] = useState<Array<OrderType>>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
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

  async function getData() {
    try {
      const allData: any = await apiCall(
        `/${restaurantName}/${tableNumber}`,
        {},
        "GET"
      );
      const data: Array<OrderType> = allData.order;
      setData(data);
    } catch (err: any) {
      alert(`Error getting in progress order: ${err.error}`);
    }
    setLoading(false);
  }
  useEffect(() => {
    getData();
  }, []);

  useEffect(() => {
    // Every 3 seconds update the state of orders
    const getNewOrders = setInterval(() => {
      getData();
    }, 3000);
    return () => clearInterval(getNewOrders);
  }, []);

  const [orderCost, setOrderCost] = useState(0);
  useEffect(() => {
    function calculateCost() {
      const initValue = 0;
      let cost = data.reduce(
        (previous: number, current: OrderType) =>
          previous + current.cost * current.quantity,
        initValue
      );
      setOrderCost(cost);
    }
    calculateCost();
  }, [data]);

  function requestBill() {
    apiCall(
      `/${restaurantName}/${tableNumber}/assistance`,
      { bill: true },
      "POST"
    )
      .then((res) => {
        console.log(res);
      })
      .catch((err) => alert(`Error requesting bill: ${err.error}`));
  }
  if (loading) {
    return (
      <Center>
        <Spinner color="purple" thickness="4px" size={"xl"} />
      </Center>
    );
  }

  return (
    <Container>
      {data.length > 0 ? (
        <>
          <TableContainer>
            <Table size="sm">
              <Thead>
                <tr>
                  <Th>Name</Th>
                  <Th>Q</Th>
                  <Th>Status</Th>
                  <Th>Cost($)</Th>
                </tr>
              </Thead>
              <Tbody>
                {data.map((item: OrderType, idx: number) => (
                  <tr key={idx}>
                    <Td>{item.name}</Td>
                    <Td>{item.quantity}</Td>
                    <Td>{item.status}</Td>
                    <Td>${item.cost}</Td>
                  </tr>
                ))}
                <tr>
                  <Td fontSize="xl">Total cost:</Td>
                  <Td></Td>
                  <Td></Td>
                  <Td fontSize="xl">${orderCost.toFixed(2)}</Td>
                </tr>
              </Tbody>
            </Table>
          </TableContainer>

          <Flex justifyContent={"flex-end"} marginBlock={"10px"}>
            <Button onClick={requestBill} colorScheme={"teal"}>
              Request Bill
            </Button>
          </Flex>
        </>
      ) : (
        <Text marginTop="10px">You have not placed any orders</Text>
      )}
    </Container>
  );
};

export default OrderProgress;
