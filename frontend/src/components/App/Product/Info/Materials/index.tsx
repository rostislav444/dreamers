import {Box, Image, Text, useMediaQuery} from '@chakra-ui/react'
import {ProductPartsInterface} from "@/interfaces/Materials";
import {InfoHeading} from "@/components/Shared/Typogrphy";


interface ProductMaterialsInterface {
    parts: ProductPartsInterface[]
    materials: { [key: number]: number };
    setSelectedMaterials: any
}

export const ProductMaterials = ({parts, materials, setSelectedMaterials}: ProductMaterialsInterface) => {
    const [mobile] = useMediaQuery('(max-width: 960px)');

    const handleMaterialsSet = (partId: number, materialId: number) => {
        const newMaterials = {...materials, [partId]: materialId}
        setSelectedMaterials(newMaterials)
    }


    return <Box mt={mobile ? 4 : 6}>
        <InfoHeading mobile={mobile}>Колір</InfoHeading>
        {parts.map(part =>
            <Box key={part.id}>
                <Text fontSize='md'>{part.name}</Text>
                {part.material_groups.map(group =>
                    <Box key={group.id}>
                        <Text fontSize='sm' mt={1} color={'orange.500'}>{group.name}</Text>
                        <Box
                            mt={mobile ? 4 : 4}
                            ml={'-9px'}
                            mb={mobile ? 4 : 6}
                        >
                            {group.materials.map(material =>
                                <Box
                                    key={material.id}
                                    position='relative'
                                    display='inline-block'
                                    m={'0 0 0 4px'}
                                    p='4px'
                                    borderWidth='2px'
                                    borderColor={materials[part.id] === material.id ? 'brown.500' : 'transparent'}
                                    borderRadius='0'
                                    cursor='pointer'
                                    _hover={{
                                        borderColor: 'orange.500'
                                    }}
                                    onClick={() => handleMaterialsSet(part.id, material.id)}
                                >
                                    {material.color && <Box w={12} h={12} bg={material.color.hex}/>}
                                    {material.material && <Box w={12} h={12}>
                                        <Image w='100%' h='100%' src={material.material.image} />
                                    </Box>}
                                </Box>
                            )}
                        </Box>
                    </Box>
                )}
            </Box>
        )
        }
    </Box>
}