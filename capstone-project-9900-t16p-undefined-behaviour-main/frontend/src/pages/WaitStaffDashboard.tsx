import { CheckIcon, CloseIcon } from "@chakra-ui/icons";
import {
  Container,
  Heading,
  Flex,
  Td,
  Tr,
  Checkbox,
  Button,
  Box,
} from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ThemeToggle from "../components/ThemeToggle";
import WaitStaffTable from "../components/WaitStaffTable";
import { apiCall, decodeRestaurantName } from "../utils/helpers";

const WaitStaffDashboard = () => {
  const { restaurantName } = useParams();
  const [deliveries, setDeliveries] = useState<Array<DDeliveryItem>>([]);
  const [prevDeliveries, setPrevDeliveries] = useState<Array<DDeliveryItem>>(
    []
  );
  const [assistance, setAssistance] = useState<Array<DAssistanceReq>>([]);
  const [prevAssistance, setPrevAssistance] = useState<Array<DAssistanceReq>>(
    []
  );

  async function deliver(
    event: React.ChangeEvent<HTMLInputElement>,
    id: number
  ) {
    if (event.target.checked === false) {
      // Cannot uncheck an item
      event.preventDefault();
      return;
    }
    apiCall(`/${restaurantName}/completeitems/${id}`, {}, "PUT").catch((err) =>
      alert(`Error marking item as delivered: ${err.error}`)
    );
  }

  async function service(
    event: React.ChangeEvent<HTMLInputElement>,
    id: number
  ) {
    apiCall(`/${restaurantName}/assistance/${id}`, {}, "PUT")
      .then((res) => console.log(res))
      .catch((err) => alert(`Error confirming the service ${err.error}`));
  }

  async function getDeliveries() {
    try {
      const data: any = await apiCall(
        `/${restaurantName}/completeitems`,
        {},
        "GET"
      );
      setDeliveries(data.complete_items);
    } catch (err: any) {
      alert(`Error fetching deliveries ${err.error}`);
    }
  }
  async function getRequests() {
    try {
      const data: any = await apiCall(
        `/${restaurantName}/assistance`,
        {},
        "GET"
      );
      setAssistance(data.assistance);
    } catch (err: any) {
      alert(`Error fetching assistance requests ${err.error}`);
    }
  }
  useEffect(() => {
    getDeliveries();
    getRequests();
  }, [restaurantName]);

  useEffect(() => {
    const updateState = setInterval(() => {
      getDeliveries();
      getRequests();
    }, 3000);
    return () => clearInterval(updateState);
  }, []);

  useEffect(() => {
    const filter = deliveries.filter(
      (x) => prevDeliveries.filter((y) => y.id === x.id).length === 0
    );
    filter.forEach(
      (newItem) =>
        new Notification(
          `Table ${newItem.table_number}: ${newItem.name} ready for delivery`
        )
    );
    setPrevDeliveries(deliveries);
  }, [deliveries]);

  useEffect(() => {
    const filter = assistance.filter(
      (x) => prevAssistance.filter((y) => y.id === x.id).length === 0
    );
    filter.forEach(
      (item) =>
        new Notification(
          `Table ${item.table_number} requests ${
            item.bill ? "their bill" : "assistance"
          }`
        )
    );
    setPrevAssistance(assistance);
  }, [assistance]);
  return (
    <Container maxWidth={"1000px"} textAlign="center">
      <Box display="flex" justifyContent={"space-between"} marginBottom={5}>
        <Heading>
          {decodeRestaurantName(restaurantName)} WaitStaff Dashboard
        </Heading>
        <ThemeToggle />
      </Box>

      {Notification.permission !== "granted" ? (
        <Button onClick={() => Notification.requestPermission()}>
          Enable Notifications
        </Button>
      ) : (
        <></>
      )}

      <Flex flexWrap={"wrap"} gap="10px">
        <WaitStaffTable
          title="Items ready to be delivered"
          headings={["Item", "Table No", "Quantity", "Item(s) Delivered"]}
          body={deliveries.map((item) => (
            <Tr key={`delivery_${item.id}`}>
              <Td textAlign={"center"}>{item.name}</Td>
              <Td textAlign={"center"}>{item.table_number}</Td>
              <Td textAlign={"center"}>{item.quantity}</Td>
              <Td textAlign={"center"}>
                <Checkbox onChange={(e) => deliver(e, item.id)} />
              </Td>
            </Tr>
          ))}
        />
        <WaitStaffTable
          title="Assistance Requests"
          headings={["Table No", "Bill Required", "Table Serviced"]}
          body={assistance.map((item) => (
            <Tr key={`assistance_${item.id}`}>
              <Td textAlign={"center"}>{item.table_number}</Td>
              <Td textAlign={"center"}>
                {item.bill ? <CheckIcon /> : <CloseIcon />}
              </Td>
              <Td textAlign={"center"}>
                <Checkbox onChange={(e) => service(e, item.id)} />
              </Td>
            </Tr>
          ))}
        />
      </Flex>
    </Container>
  );
};

export default WaitStaffDashboard;
