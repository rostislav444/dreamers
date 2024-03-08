import {Box, Table, TableContainer, Tbody, Td, Tr} from '@chakra-ui/react'
import {ProductInterface} from "@/interfaces/Product";
import {InfoHeading} from "@/components/Shared/Typogrphy";
import {selectedMaterialsInterface} from "@/components/App/Product";

interface ProductCharacteristicsProps {
    product: ProductInterface,
    selectedMaterials: selectedMaterialsInterface
}


const TdStyledLeft = ({children}: { children: any }) => <Td w={52} px={0} pb={3} borderBottom="none">{children}</Td>
const TdStyled = ({children}: { children: any }) => <Td px={0} pb={3} borderBottom="none">{children}</Td>

export const ProductCharacteristics = ({product, selectedMaterials}: ProductCharacteristicsProps) => {

    const selectedParts = product.parts.map(part => ({
        name: part.name,
        material: part.material_groups.flatMap(group => group.materials.find(
            material => material.id === selectedMaterials[part.id]
        ))[0]
    }))


    return <Box>
        <InfoHeading>Характеристики</InfoHeading>
        <Box mt='4'>
            <TableContainer>
                <Table size='sm'>
                    <Tbody>
                        <Tr>
                            <TdStyledLeft>Ширина</TdStyledLeft>
                            <TdStyled>{product.width} см.</TdStyled>
                        </Tr>
                        <Tr>
                            <TdStyledLeft>Висота</TdStyledLeft>
                            <TdStyled>{product.height} см.</TdStyled>
                        </Tr>
                        <Tr>
                            <TdStyledLeft>Глибина</TdStyledLeft>
                            <TdStyled>{product.depth} см.</TdStyled>
                        </Tr>
                        {...selectedParts.map((mat, key) => <Tr key={key}>
                            <TdStyledLeft>{mat.name}</TdStyledLeft>
                            {mat.material && <TdStyled>{mat.material?.color?.name}</TdStyled>}

                        </Tr>)}
                    </Tbody>
                </Table>
            </TableContainer>
        </Box>

    </Box>
}

