import {Box, Heading, Table, TableContainer, Tbody, Td, Tr} from '@chakra-ui/react'
import {ProductInterface} from "@/interfaces/Product";
import {InfoHeading} from "@/components/Shared/Typogrphy";

interface ProductCharacteristicsProps {
    product: ProductInterface
}


const TdStyled = ({children}: { children: any }) => <Td
    px={0}
    pb={3}
    borderBottom="none"
>{children}</Td>


export const ProductCharacteristics = ({product}: ProductCharacteristicsProps) => {
    return <Box>
        <InfoHeading>Характеристики</InfoHeading>
        <Box mt='4' >
            <TableContainer>
                <Table size='sm'>
                    <Tbody>
                        <Tr>
                            <TdStyled>Ширина</TdStyled>
                            <TdStyled>{product.width} см.</TdStyled>
                        </Tr>
                        <Tr>
                            <TdStyled>Висота</TdStyled>
                            <TdStyled>{product.height} см.</TdStyled>
                        </Tr>
                        <Tr>
                            <TdStyled>Глибина</TdStyled>
                            <TdStyled>{product.depth} см.</TdStyled>
                        </Tr>
                    </Tbody>
                </Table>
            </TableContainer>
        </Box>

    </Box>
}

