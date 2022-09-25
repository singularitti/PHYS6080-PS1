using StaticArrays: SVector, MVector

export Particle
export distance, potential_energy, force, distribute!, initialize!

mutable struct Particle
    r::MVector{3,Float64}
    v::MVector{3,Float64}
    Particle() = new()  # Incomplete initialization
end

struct Particles{N}
    data::SVector{N,Particle}
end

function distance(particle1::Particle, particle2::Particle)
    @assert particle1.r != particle2.r "the two particles crashed!"
    return sqrt(sum(abs2, particle1.r - particle2.r))
end

function potential_energy(particle1::Particle, particle2::Particle)
    r = distance(particle1, particle2)
    η = 1 / r^6
    return 4ε * η * (η - 1)
end
function potential_energy(particles::Particles)
    total = 0
    for (i, particleᵢ) in enumerate(particles)
        for particleⱼ in particles[i:end]
            total += potential_energy(particleᵢ, particleⱼ)
        end
    end
    return 2total
end

function force(p1::Particle, p2::Particle)
    η = 1 / distance(p1, p2)
    return (p1.r - p2.r) * (η^14 - η^8)
end
function force(particles, i)
    @assert length(particles) > 1 "you must have more than 1 particle to calculate the force!"
    particleᵢ = particles[i]
    return sum(enumerate(particles)) do (j, particleⱼ)
        j != i ? force(particleᵢ, particleⱼ) : zeros(MVector{3,Float64})
    end
end
force(particles) = sum(map(Base.Fix1(force, particles), eachindex(particles)))

acceleration(particles, i) = force(particles, i)
acceleration(particles) = force(particles)

function distribute!(particles, volume)
    @assert length(particles) > 0
    n, a = length(particles), cbrt(volume)
    for (particle, coordinates) in zip(particles, eachcol(a * rand(3, n)))
        particle.r = coordinates
    end
    @assert unique(particles) == particles
    return particles
end

function initialize!(particles)
    @assert length(particles) > 0
    for particle in particles
        particle.v = zeros(MVector{3,Float64})
    end
    return particles
end

# Similar to https://github.com/JuliaCollections/IterTools.jl/blob/0ecaa88/src/IterTools.jl#L1028-L1032
function Base.iterate(iter::Particles, state=1)
    if state > length(iter)
        return nothing
    else
        return iter.data[state], state + 1
    end
end

Base.eltype(::Particles) = Particle

Base.length(iter::Particles) = length(iter.data)

Base.IteratorSize(::Type{<:Particles}) = Base.HasLength()

Base.getindex(iter::Particles, i...) = getindex(iter.data, i...)

Base.firstindex(::Particles) = 1

Base.lastindex(iter::Particles) = length(iter)
