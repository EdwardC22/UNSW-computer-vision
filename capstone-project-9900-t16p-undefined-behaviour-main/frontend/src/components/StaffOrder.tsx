import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Table,
  TableContainer,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import InteractableOrderItem from "./InteractableOrderItem";

/// Component wraps an accordion item to provide kitchen staff information
/// and ability to update status of items

interface Props {
  order: DOrderType;
}

const StaffOrder = ({ order }: Props) => {
  const date = new Date(order.submit_time);
  const [minutesAgo, setMinutesAgo] = useState<number | undefined>(undefined);

  useEffect(() => {
    const updateTimer = setInterval(() => {
      const currentTime = Date.now();
      const diff = currentTime - date.getTime();
      const mins = Math.floor(diff / 1000 / 60);
      setMinutesAgo(mins);
    }, 1000);
    return () => clearInterval(updateTimer);
  }, []);

  return (
    <AccordionItem>
      <h2>
        <AccordionButton>
          <Box flex="1" textAlign={"left"} display="flex" flexDir="row">
            <Box>Table {order.table_number} | </Box>
            <Box>
              Order placed: {date.toLocaleTimeString()} | {minutesAgo} minutes
              ago
            </Box>
          </Box>
          <AccordionIcon />
        </AccordionButton>
      </h2>
      <AccordionPanel>
        <TableContainer overflowX={"hidden"}>
          <Table>
            <Thead>
              <Tr>
                <Th>Name</Th>
                <Th>Quantity</Th>
                <Th>In progress?</Th>
                <Th>Ready for delivery?</Th>
              </Tr>
            </Thead>
            {order.items.map((item) => (
              <InteractableOrderItem item={item} key={item.id} />
            ))}
          </Table>
        </TableContainer>
      </AccordionPanel>
    </AccordionItem>
  );
};
export default StaffOrder;
