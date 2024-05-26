import { DeleteIcon } from "@chakra-ui/icons";
import { Button } from "@chakra-ui/react";

/// Wrapper for a generic red delete button

interface Props {
  clickHandler: any;
}
const DeleteButton = ({ clickHandler }: Props) => {
  return (
    <Button
      colorScheme="red"
      rightIcon={<DeleteIcon />}
      variant="outline"
      onClick={clickHandler}
    >
      Delete
    </Button>
  );
};

export default DeleteButton;
