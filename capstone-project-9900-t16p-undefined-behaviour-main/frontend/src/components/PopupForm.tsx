import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
} from "@chakra-ui/react";
import * as React from "react";

/// Component wraps a chakra ui modal. Excepts a form as a component to render
/// and handle user input

interface Props {
  handleClose: Function;
  open: boolean;
  formState?: DPopupFormState;
}

const PopupForm = (props: Props) => {
  return (
    <>
      <Modal isOpen={props.open} onClose={() => props.handleClose()}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{props.formState?.title}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>{props.formState?.form}</ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default PopupForm;
