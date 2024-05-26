import { Checkbox, Tbody, Td, Tr } from "@chakra-ui/react";
import { useState } from "react";
import { useParams } from "react-router-dom";
import { apiCall } from "../utils/helpers";

/// Component wraps a table row.
/// Component is used inside of the kitchen staff table to display information
/// as well as update the progress of the item

interface Props {
  item: DStaffOrderItem;
}

const InteractableOrderItem = ({ item }: Props) => {
  const { restaurantName } = useParams();
  const [inProgress, setInProgress] = useState<boolean>(item.in_progress > 0);
  const [isComplete, setIsComplete] = useState<boolean>(item.in_progress > 1);

  async function submitProgress(ev: boolean) {
    try {
      await apiCall(`/${restaurantName}/ordereditems/${item.id}`, {}, "PUT");
      setInProgress(true);
    } catch (err) {
      alert(`Error updating progress ${err}`);
    }
  }

  async function submitCompletion(ev: boolean) {
    try {
      await apiCall(`/${restaurantName}/inprogessitems/${item.id}`, {}, "PUT");
      setIsComplete(true);
    } catch (err) {
      alert(`Error updating completion ${err}`);
    }
  }
  return (
    <Tbody>
      <Tr>
        <Td>{item.name}</Td>
        <Td>{item.quantity}</Td>
        <Td>
          <Checkbox
            isChecked={inProgress}
            disabled={inProgress}
            onChange={(e) => submitProgress(e.target.checked)}
          />
        </Td>
        <Td>
          <Checkbox
            isChecked={isComplete}
            disabled={isComplete || !inProgress}
            onChange={(e) => submitCompletion(e.target.checked)}
          />
        </Td>
      </Tr>
    </Tbody>
  );
};
export default InteractableOrderItem;
