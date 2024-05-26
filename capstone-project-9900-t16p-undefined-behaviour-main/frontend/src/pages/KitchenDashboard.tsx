import { Accordion, Box, Container, Heading, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import StaffOrder from "../components/StaffOrder";
import ThemeToggle from "../components/ThemeToggle";
import { apiCall, decodeRestaurantName } from "../utils/helpers";

const KitchenDashboard = () => {
  const { restaurantName } = useParams();
  const [orders, setOrders] = useState<Array<DOrderType>>([]);
  useEffect(() => {
    getOrders();
  }, []);

  async function getOrders() {
    try {
      const data: any = await apiCall(`/${restaurantName}/orders`, {}, "GET");
      setOrders(data.orders);
    } catch (err: any) {
      alert(`Error fetching orders ${err.error}`);
    }
  }

  useEffect(() => {
    // Every 3 seconds update the state of orders
    const getNewOrders = setInterval(() => {
      getOrders();
    }, 3000);
    return () => clearInterval(getNewOrders);
  }, []);
  return (
    <Container maxWidth={"650px"}>
      <Box display="flex" justifyContent={"space-between"} marginBottom={5}>
        <Heading>
          {decodeRestaurantName(restaurantName)} Kitchen Dashboard
        </Heading>
        <ThemeToggle />
      </Box>
      {orders.length > 0 ? (
        <Container maxWidth={"650px"}>
          <Accordion allowMultiple defaultIndex={[0]}>
            {orders.map((order) => (
              <StaffOrder order={order} key={order.id} />
            ))}
          </Accordion>
        </Container>
      ) : (
        <Text>No current orders</Text>
      )}
    </Container>
  );
};

export default KitchenDashboard;
