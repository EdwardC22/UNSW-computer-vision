
interface DItem {
  id: number;
  name: string;
  description: string;
  ingredients: string;
  image: string;
  cost: number;
  category_pos: number;
  popular: boolean;
}


interface DPopupFormState {
  title: string;
  form: Formik;
}


interface DCategory {
  id: number;
  items: Array<DItem>;
  name: string;
  restaurant_pos: number;
}

interface DStaffOrderItem {
  id: number;
  in_progress: number;
  name: string;
  quantity: number;
}

interface DOrderType {
  id: number;
  items: Array<StaffOrderItem>;
  submit_time: Date;
  table_number: number;
}


interface DDeliveryItem {
  name: string;
  id: number;
  table_number: number;
  quantity: number;
  boolean: boolean;
}

interface DAssistanceReq {
  table_number: number;
  bill: boolean;
  id: number;
}