interface Question {
    question: string,
    rvs: RandomVariable[],
    pvs: ProcessedVariables,
    answer_expressions: ProcessedVariables
    answer: string
}

interface RandomVariable {
    name: string,
    lb: number,
    hb: number
}

interface ProcessedVariables {
    [variable: string]: string // evalString
}

interface EvaluatedRVs {
    [name: string]: number // value
}

interface Category {
    id: string,
    title: string,
    description: string,
    imageLink: string,
    tags: string[],
    author: string,
    questions: string[]
}
