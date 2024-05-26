import { Container, Heading, Select } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { apiCall, decodeRestaurantName } from "../utils/helpers";

/// Component used to allow customers to select which table they are seated at

const MenuTableSelect = () => {
  const [tableCount, setTableCount] = useState<number | undefined>(undefined);
  const { restaurantName, tableNumber } = useParams();
  const [stateTableNumber, setStateTableNumber] = useState<undefined | number>(
    tableNumber === undefined ? undefined : parseInt(tableNumber)
  );
  const navigate = useNavigate();

  useEffect(() => {
    async function getTableCount() {
      apiCall(`/${restaurantName}/tables`, {}, "GET")
        .then((res: any) => {
          if (res.tables === null) {
            alert("Restaurant does not exist");
            return;
          }
          setTableCount(res.tables);
        })
        .catch((err) => console.log(err));
    }
    getTableCount();
  }, []);

  useEffect(() => {
    // Ensure URL is up to date
    if (stateTableNumber !== undefined) {
      navigate(`${stateTableNumber}`);
    } else {
      navigate(`/${restaurantName}/order/`);
    }
  }, [stateTableNumber]);

  // Let customer pick table
  return (
    <Container>
      <Heading>Order {decodeRestaurantName(restaurantName)}</Heading>
      <Select
        placeholder="Select your table"
        onChange={(ev) => {
          setStateTableNumber(parseInt(ev.target.value));
        }}
      >
        {Array(tableCount)
          .fill(0)
          .map((_, idx) => (
            <option key={idx} value={idx + 1}>
              Table {idx + 1}
            </option>
          ))}
      </Select>
    </Container>
  );
};

export default MenuTableSelect;
