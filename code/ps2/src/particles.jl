using StaticArrays: MVector

export Particle
export distance, potential, force

mutable struct Particle
    r::MVector{3,Float64}
    v::MVector{3,Float64}
end

function distance(p1::Particle, p2::Particle)
    @assert p1.r != p2.r "the two particles crashed!"
    return sqrt(sum(abs2, p1.r - p2.r))
end

function potential(p1::Particle, p2::Particle)
    r = distance(p1, p2)
    η = (σ / r)^6
    return 4ε * η * (η - 1)
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
force(particles) = map(Base.Fix1(force, particles), eachindex(particles))
