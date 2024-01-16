import {Box, Flex, Text} from "@chakra-ui/react";
import {addSpacesToNumber} from "@/utils/numbers";

interface OrderTotalProps {
    mobile: boolean,
    calculateTotalQty: () => number,
    calculateTotal: () => number
}


interface WrapperProps {
    children: any,
    mobile: boolean,
}


const Wrapper = ({children, mobile}: WrapperProps) => {
    return mobile ?
        <Flex mt='8' pt='6' pb={6} flexDirection='column' justifyContent='center' alignItems='center' bg='#ffffff85' border='4px solid'
              borderColor='brown.500'>{children}</Flex> :
        <Box mt='8'>{children}</Box>
}

export const OrderTotal = ({mobile, calculateTotalQty, calculateTotal}: OrderTotalProps) =>
    <Wrapper mobile={mobile}>
        <Text fontSize='24'>Всього товарів: {calculateTotalQty()} шт.</Text>
        <Text fontSize='24' mt={2}>Сума: {addSpacesToNumber(calculateTotal())} грн.</Text>
    </Wrapper>
